from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLE_MODERATOR = 0
    ROLE_ADMIN = 1

    ROLE_CHOICES = (
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'),
    )

    password = None
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)
    bio = models.CharField('User bio', max_length=256, blank=True, null=True)
    confirmation_code = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(10000), MaxValueValidator(99999)]
    )
    is_email_confirmed = models.BooleanField(default=False)
