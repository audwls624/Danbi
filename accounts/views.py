from rest_framework.views import APIView
from .serializers import UserSerializer
from .constants import RESPONSE_MESSAGE_REGISTER_SUCCESS, RESPONSE_MESSAGE_LOGIN_SUCCESS, RESPONSE_MESSAGE_LOGOUT_SUCCESS
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        result = dict()
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        result.update(
            user=serializer.data.get('email'),
            message=RESPONSE_MESSAGE_REGISTER_SUCCESS,
        )
        return Response(result, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        user_email = request.data.get('email')
        user_password = request.data.get('password')
        user = authenticate(request, email=user_email, password=user_password)
        result = dict()

        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        result.update(
            user=serializer.data.get('email'),
            message=RESPONSE_MESSAGE_LOGIN_SUCCESS,
            token=dict(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
        )
        res = Response(result, status=status.HTTP_200_OK)
        res.set_cookie("access_token", access_token, httponly=True)
        res.set_cookie("refresh_token", refresh_token, httponly=True)
        return res


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            res = Response(dict(message=RESPONSE_MESSAGE_LOGOUT_SUCCESS), status=status.HTTP_202_ACCEPTED)
            res.delete_cookie('access_token')
            res.delete_cookie('refresh_token')
            return res
        except Exception as e:
            return Response(dict(message=str(e)), status=status.HTTP_401_UNAUTHORIZED)


