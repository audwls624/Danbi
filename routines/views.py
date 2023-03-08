from datetime import datetime, timedelta
from .models import Routine, RoutineResult, RoutineDay
from .serializers import RoutineSerializer, RoutineResultSerializer, RoutineDaySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from common.constants import STATUS_MESSAGE_ROUTINE_CREATE_OK, RESPONSE_MESSAGE_ROUTINE_CREATE_SUCCESS, DATE_STRING_YYYYMMDD


class RoutineInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        request_date = request.query_params.get('today')
        result = dict()

        if not request_date:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        query_set = RoutineResult.get_rountine_result_qs_by_date(request_date, request.user.id)
        serializer = RoutineResultSerializer(data=list(query_set), many=True)
        if not serializer.is_valid():
            result.update(message=serializer.errors)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        routine_days = request_data.get('days')
        request_data.update(account=request.user.id)
        request_data.pop('days')
        result = dict()

        routine_serializer = RoutineSerializer(data=request_data)
        if not routine_serializer.is_valid() or not routine_days:
            result.update(message=routine_serializer.errors)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        routine_serializer.save()
        routine_id = routine_serializer.data.get('id')
        routine_day_data = [dict(day=day, routine_id=routine_id) for day in routine_days]
        routine_day_serializer = RoutineDaySerializer(data=routine_day_data, many=True)

        if not routine_day_serializer.is_valid() or not routine_days:
            result.update(message=routine_day_serializer.errors)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        routine_day_serializer.save()

        result.update(
            data=dict(routine_id=routine_id),
            message=dict(
                msg=RESPONSE_MESSAGE_ROUTINE_CREATE_SUCCESS,
                status=STATUS_MESSAGE_ROUTINE_CREATE_OK,
            )
        )
        return Response(result, status=status.HTTP_201_CREATED)
