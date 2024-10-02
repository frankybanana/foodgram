from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from backend.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH


class User(AbstractUser):

    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name='email'
    )
    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        verbose_name='Ник пользователя',
        validators=(RegexValidator(r'^[\w.@+-]+\Z'),),
    )
    first_name = models.CharField(max_length=MAX_USERNAME_LENGTH, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=MAX_USERNAME_LENGTH, verbose_name='Фамилия пользователя')
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH)
    avatar = models.ImageField(
        upload_to='users/images/',
        null=True,
        default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password', ]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='follower',
        verbose_name='подписчик',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='author',
        verbose_name='автор',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='unique_following'
            )
        ]

    def __str__(self):
        return f'{self.follower} - {self.author}'
