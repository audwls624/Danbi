import pytz
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from .models import Routine, RoutineDay, RoutineResult
from danbi import settings
from .serializers import RoutineResultSerializer
from common.constants import RESPONSE_MESSAGE_REGISTER_SUCCESS, RESPONSE_MESSAGE_LOGIN_SUCCESS, RESPONSE_MESSAGE_LOGOUT_SUCCESS, DATE_STRING_YYYYMMDD


class RoutineCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='passworD12$'
        )
        self.client.force_authenticate(user=self.user)

    def test_routine_create_test(self):
        request_data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": '["MON", "WED", "FRI"]',
        }

        response = self.client.post(reverse('routines:info_view'), data=request_data)
        print(response.data.get('message'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RoutineResultRetrieveTestCase(APITestCase):
    def setUp(self):

        target_date = datetime(year=2022, month=2, day=14, tzinfo=pytz.timezone(settings.TIME_ZONE))
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='passworD12$',
        )

        self.client.force_authenticate(user=self.user)
        self.routine_1 = Routine.objects.create(
            account=self.user,
            title='Test Routine',
            category='HOMEWORK',
            goal='Test goal',
            is_alarm=True,
        )
        self.routine_2 = Routine.objects.create(
            account=self.user,
            title='Test Routine',
            category='MIRACLE',
            goal='Test goal',
            is_alarm=True,
        )
        self.routine_day = RoutineDay.objects.create(
            routine=self.routine_1,
            day='MON'
        )
        self.routine_result = RoutineResult.objects.create(
            routine=self.routine_1,
            result=True
        )
        self.routine_day_2 = RoutineDay.objects.create(
            routine=self.routine_2,
            created_at=target_date,
            day='MON',
        )
        self.routine_result_2 = RoutineResult.objects.create(
            routine=self.routine_2,
            result=True
        )

    def test_routine_result_retrieve(self):
        target_date = '2022-02-14'
        response = self.client.get(reverse('routines:info_view') + f'?today={target_date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

