from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from api.v1 import permissions

User = get_user_model()


class UserListView(generics.ListAPIView):
    """ Список пользователей """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.CustomUserShortSerializer
    permission_classes = [permissions.AdminPermission]


class UserCreateView(generics.CreateAPIView):
    """ Создать клиент """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.CustomUserCreateSerializer
    permission_classes = [permissions.AllowAllPermission]


class SupplierCreateView(generics.CreateAPIView):
    """ Создать поставщик """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.WorkerCreateSerializer
    permission_classes = [permissions.AdminPermission]


class AuthorCreateView(generics.CreateAPIView):
    """ Создать автор """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.WorkerCreateSerializer
    permission_classes = [permissions.AdminPermission]


class AdminCreateView(generics.CreateAPIView):
    """ Создать админ """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.WorkerCreateSerializer
    permission_classes = [permissions.AdminPermission]


class UserUpdateView(generics.UpdateAPIView):
    """ Редактировать пользователя """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.CustomUserShortSerializer
    permission_classes = [permissions.AdminPermission]


class UserDetailView(generics.RetrieveAPIView):
    """ О пользователе подробно """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.CustomUserDetailSerializer
    permission_classes = [permissions.AllowAllPermission]

    def get_object(self):
        if self.request.user.role == User.Role.CLIENT:
            return self.request.user
        return super().get_object()


class UserDeleteView(generics.DestroyAPIView):
    """ Удалить пользователя """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.CustomUserShortSerializer
    permission_classes = [permissions.AdminPermission]


