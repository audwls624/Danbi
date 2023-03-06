import re
from .models import User
from .constants import PASSWORD_REGEX
from rest_framework import serializers
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[RegexValidator(PASSWORD_REGEX)])

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def validate_password(self, password):
    #     if not re.fullmatch(PASSWORD_REGEX, password):
    #         raise ValueError("잘못된 비밀번호입니다")
    #     return password

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
