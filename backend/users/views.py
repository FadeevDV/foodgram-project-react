from uuid import uuid1

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from .models import User
from .serializers import (UserEmailSerializer, UserLoginSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Модель обработки запросов пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = permissions.IsAuthenticated
    lookup_field = 'username'

    @action(
        detail=False, methods=['PATCH', 'GET'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmationCodeView(APIView):

    def post(self, request):
        """Обработка POST запроса на получение Confirmation code"""
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        secret = str(uuid1())  # генерация уникального ключа
        User.objects.create(email=email, secret=secret)
        send_mail(
            'Ваш секретный код',
            secret,
            settings.ADMIN_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """ Модель авторизации пользователя """

    def post(self, request):
        """
        Обработка POST запроса на получение JWT по email и секретному коду
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']

        user = get_object_or_404(User, email=email)

        refresh = RefreshToken.for_user(user)  # получаем токен

        return Response(
            {"access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
