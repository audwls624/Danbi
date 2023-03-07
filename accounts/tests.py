from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .constants import RESPONSE_MESSAGE_REGISTER_SUCCESS, RESPONSE_MESSAGE_LOGIN_SUCCESS, RESPONSE_MESSAGE_LOGOUT_SUCCESS


class RegisterTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:register_view')

    def test_register_success(self):
        data = {
            "email": "test@test.com",
            "password": "Test1234!@#$",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'), 'register success')
        self.assertEqual(response.data.get('user'), 'test@test.com')

    def test_register_short_password(self):
        data = {
            "email": "test@test.com",
            "password": "short",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_password(self):
        data = {
            "email": "test@test.com",
            "password": "test123d",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Test1234!',
        )
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.access_token = str(RefreshToken.for_user(self.user).access_token)

    def test_login_view(self):
        url = reverse('accounts:login_view')
        data = {
            'email': self.user.email,
            'password': 'Test1234!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], RESPONSE_MESSAGE_LOGIN_SUCCESS)
        self.assertEqual(response.data['user'], self.user.email)
        self.assertTrue('access_token' in response.data['token'])
        self.assertTrue('refresh_token' in response.data['token'])
        self.assertTrue(response.cookies['access_token'])
        self.assertTrue(response.cookies['refresh_token'])

    def test_login_with_invalid_credentials(self):
        url = reverse('accounts:login_view')
        data = {'email': 'invalid@test.com', 'password': 'password'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='passworD12$'
        )

    def test_logout_with_valid_token(self):
        login_data = {'email': 'testuser@example.com', 'password': 'passworD12$'}
        login_response = self.client.post(reverse('accounts:login_view'), data=login_data)
        access_token = login_response.data['token']['access_token']
        refresh_token = login_response.data['token']['refresh_token']

        self.client.cookies['access_token'] = access_token
        self.client.cookies['refresh_token'] = refresh_token
        response = self.client.get(reverse('accounts:logout_view'))

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(str(response.cookies.get('access_token').value), '')
        self.assertEqual(str(response.cookies.get('refresh_token').value), '')

    def test_logout_with_invalid_token(self):
        self.client.cookies['refresh_token'] = 'invalid-token'
        response = self.client.get(reverse('accounts:logout_view'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


