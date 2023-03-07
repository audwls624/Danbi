from rest_framework import serializers
from .models import Routine, RoutineResult, RoutineDay


class RoutineSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Routine.CHOICES_CATEGORY)

    def validate_category(self, value):
        if value not in dict(Routine.CHOICES_CATEGORY):
            raise serializers.ValidationError('Invalid Category')
        return value

    class Meta:
        model = Routine
        exclude = ('created_at', 'modified_at', 'is_deleted')


class RoutineResultSerializer(serializers.ModelSerializer):
    routine_key = RoutineSerializer(read_only=True)

    class Meta:
        model = RoutineResult
        exclude = ('created_at', 'modified_at', 'is_deleted')


class RoutineDaySerializer(serializers.ModelSerializer):
    day = serializers.ChoiceField(choices=RoutineDay.CHOICES_DAYS)

    def validate_day(self, value):
        if value not in dict(RoutineDay.CHOICES_DAYS):
            raise serializers.ValidationError('Invalid Day')
        return value

    class Meta:
        model = RoutineDay
        fields = ('day', 'routine_id')
