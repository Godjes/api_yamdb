from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_MODERATOR = 0
    ROLE_ADMIN = 1

    ROLE_CHOICES = (
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'),
    )

    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)
    bio = models.CharField('User bio', max_length=256, blank=True, null=True)
