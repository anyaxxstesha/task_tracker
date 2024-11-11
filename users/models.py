from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """User model"""
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='email address'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        help_text='Укажите имя',
        **NULLABLE
    )
    lastname = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        help_text='Укажите фамилию',
        **NULLABLE
    )
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        help_text='Введите номер телефона',
        **NULLABLE
    )
    country = CountryField(
        verbose_name='Страна',
        help_text='Выберите страну',
        **NULLABLE
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        help_text='Загрузите аватар',
        **NULLABLE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.email
