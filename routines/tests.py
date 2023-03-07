from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import User
from accounts.constants import RESPONSE_MESSAGE_REGISTER_SUCCESS, RESPONSE_MESSAGE_LOGIN_SUCCESS, RESPONSE_MESSAGE_LOGOUT_SUCCESS


class RoutineCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='passworD12$'
        )
        self.client.force_authenticate(user=self.user)

    def test_routine_test(self):
        request_data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        response = self.client.post(reverse('routines:info_view'), data=request_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

