from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from core.constants import (
    MAX_TAG_LENGTH,
    MAX_SLUG_LENGTH,
)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=MAX_TAG_LENGTH,
                            unique=True,
                            verbose_name='Тег')
    slug = models.SlugField(max_length=MAX_SLUG_LENGTH,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)
        unique_together = ('name', 'slug')

    def __str__(self):
        return f"{self.name}"