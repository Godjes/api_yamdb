from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLE_MODERATOR = 'M'
    ROLE_ADMIN = 'A'
    ROLE_USER = 'U'

    ROLE_CHOICES = (
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'),
        (ROLE_USER, 'user')
    )

    password = None
    role = models.CharField(
        choices=ROLE_CHOICES, default=ROLE_USER,
        max_length=1)
    bio = models.CharField('User bio', max_length=256, blank=True, null=True)
    confirmation_code = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(10000), MaxValueValidator(99999)]
    )
    is_email_confirmed = models.BooleanField(default=False)
