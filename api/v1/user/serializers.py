from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from common.models import AcceptOrder

User = get_user_model()


class CustomUserCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all(),
                        message="Эта электронная почта зарегистрирован",
                        )])

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'phone',
            'address'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
            'phone': {'required': True},
            'address': {'required': True},
        }


class WorkerCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all(),
                        message="Эта электронная почта зарегистрирован",
                        )])

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'role',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
        }


class CustomUserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
        ]


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'role',
            'is_staff',
            'is_superuser',
            'is_active',
            'last_login',
            'date_joined',
            'phone',
            'gender',
            'address'
        ]

    def to_representation(self, instance):
        from api.v1.common.serializers import AcceptOrderSerializer
        context = super().to_representation(instance)
        qs = AcceptOrder.objects.filter(is_active=True, order__customer=instance)
        context['buy_books'] = AcceptOrderSerializer(qs, many=True).data
        return context
