from typing import Optional
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> 'CustomUser':
        if not email:
            raise ValueError('Email является обязательным полем')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user  # type: ignore[return-value]

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields) -> 'CustomUser':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # type: ignore[assignment, misc]

    email = models.EmailField('Электронная почта', unique=True)
    phone = models.CharField('Номер телефона', max_length=20, blank=True, null=True)
    patronymic = models.CharField('Отчество', max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects: CustomUserManager = CustomUserManager()  # type: ignore[assignment, misc]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name or ''} ({self.email})".strip()
