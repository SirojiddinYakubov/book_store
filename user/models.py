from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.v1.user.validators import validate_phone
from user.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Gender(models.IntegerChoices):
        MAN = 0, _('Мужчина')
        WOMAN = 1, _('Женщина')

    class Role(models.IntegerChoices):
        CLIENT = 0, _('Клиент')
        SUPPLIER = 1, _('Поставщик')
        AUTHOR = 2, _('Автор')
        ADMIN = 3, _('Администратор')

    username = None
    email = models.EmailField(verbose_name=_('Электронная почта'), unique=True)

    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=255, blank=True)
    first_name = models.CharField(verbose_name=_('Имя'), max_length=255, blank=True)
    middle_name = models.CharField(verbose_name=_('Отчество'), max_length=255, blank=True)
    role = models.IntegerField(verbose_name=_('Рол'), choices=Role.choices, default=Role.CLIENT)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(verbose_name=_('Телефон номер'), max_length=12, validators=[validate_phone], blank=True)
    gender = models.IntegerField(verbose_name=_('Пол'), choices=Gender.choices, default=Gender.MAN)
    address = models.CharField(verbose_name=_('Адрес'), max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.last_name and self.first_name and self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        else:
            return self.email

    @property
    def fullname(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"