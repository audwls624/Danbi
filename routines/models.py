import pytz
from datetime import datetime, timedelta


from django.db import models
from accounts.models import User
from common.constants import DATE_STRING_YYYYMMDD
from danbi import settings


class Routine(models.Model):
    CATEGORY_MIRACLE = 'MIRACLE'
    CATEGORY_HOMEWORK = 'HOMEWORK'
    CHOICES_CATEGORY = (
        (CATEGORY_MIRACLE, '기상'),
        (CATEGORY_HOMEWORK, '숙제'),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='수정 일시')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='제목')
    category = models.CharField(max_length=100, choices=CHOICES_CATEGORY, null=True, blank=True, verbose_name='카테고리')
    goal = models.CharField(max_length=255, null=True, blank=True, verbose_name='목표')
    is_alarm = models.BooleanField(default=False, verbose_name='알림 여부')
    is_deleted = models.BooleanField(default=False, verbose_name='삭제 여부')
    account = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='유저 ID')

    class Meta:
        db_table = 'routine'
        verbose_name = '할 일'


class RoutineResult(models.Model):
    RESULT_NOT = 'NOT'
    RESULT_TRY = 'TRY'
    RESULT_DONE = 'DONE'
    CHOICES_RESULT = (
        (RESULT_NOT, '안함'),
        (RESULT_TRY, '시도'),
        (RESULT_DONE, '완료'),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='수정 일시')
    is_deleted = models.BooleanField(default=False, verbose_name='삭제 여부')
    result = models.CharField(max_length=100, choices=CHOICES_RESULT, null=True, blank=True, verbose_name='결과')
    routine = models.ForeignKey(Routine, on_delete=models.DO_NOTHING, verbose_name='할 일 ID')

    @staticmethod
    def get_rountine_result_qs_by_date(target_date_str, user_id):
        datetime_obj = datetime.strptime(target_date_str, DATE_STRING_YYYYMMDD)
        target_date = datetime_obj.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        weekday = RoutineDay.WEEK_DAY_LIST[target_date.weekday()]
        routine_id_list = list(Routine.objects.filter(account=user_id, routineday__day=weekday).values_list('id', flat=True))
        query_set = RoutineResult.objects.filter(
            created_at__gte=target_date,
            created_at__lt=target_date + timedelta(days=1),
            routine__in=routine_id_list)
        return query_set

    class Meta:
        db_table = 'routine_result'
        verbose_name = '할 일 수행 결과'


class RoutineDay(models.Model):
    CHOICE_MON = 'MON'
    CHOICE_TUE = 'TUE'
    CHOICE_WED = 'WEB'
    CHOICE_THU = 'THU'
    CHOICE_FRI = 'FRI'
    CHOICE_SAT = 'SAT'
    CHOICE_SUN = 'SUN'
    CHOICES_DAYS = (
        (CHOICE_MON, '월요일'),
        (CHOICE_TUE, '화요일'),
        (CHOICE_WED, '수요일'),
        (CHOICE_THU, '목요일'),
        (CHOICE_FRI, '금요일'),
        (CHOICE_SAT, '토요일'),
        (CHOICE_SUN, '일요일'),
    )
    WEEK_DAY_LIST = [
        CHOICE_MON,
        CHOICE_TUE,
        CHOICE_WED,
        CHOICE_THU,
        CHOICE_FRI,
        CHOICE_SAT,
        CHOICE_SUN,
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='수정 일시')
    day = models.CharField(max_length=100, choices=CHOICES_DAYS, null=True, blank=True, verbose_name='요일')
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, verbose_name='할 일 ID')

    class Meta:
        db_table = 'routine_day'
        verbose_name = '할 일 '
