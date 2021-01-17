from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    middle_name = models.CharField(max_length=20, verbose_name='отчество')
    phone_number = models.CharField(max_length=20, verbose_name='телефон')
    address = models.CharField(max_length=200, verbose_name='адрес')

    def __str__(self):
        return str(self.username)