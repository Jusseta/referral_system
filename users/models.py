from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """User model"""
    username = None
    password = None
    phone = models.CharField(unique=True, max_length=20, verbose_name='phone number')
    auth_code = models.IntegerField(verbose_name='authorization code', **NULLABLE)
    invite_code = models.CharField(unique=True, max_length=10, verbose_name='invite code', **NULLABLE)
    used_invite_code = models.CharField(max_length=10, verbose_name="other's invite code", **NULLABLE)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.phone}'
