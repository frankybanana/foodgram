from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import MAX_EMAIL_LENGTH, MAX_USER_NAME_LENGTH


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH,
                              unique=True,
                              verbose_name='email')
    first_name = models.CharField(max_length=MAX_USER_NAME_LENGTH,
                                  verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=MAX_USER_NAME_LENGTH,
                                 verbose_name='Фамилия пользователя')
    avatar = models.ImageField(upload_to='users/images/',
                               blank=True,
                               default=None)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser
