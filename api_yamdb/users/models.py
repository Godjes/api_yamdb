from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'


class User(AbstractUser):
    """Класс переопределения базового user"""

    ROLE_CHOICES = (
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'),
        (ROLE_USER, 'user')
    )

    password = None
    role = models.CharField(
        choices=ROLE_CHOICES, default=ROLE_USER,
        max_length=9)
    bio = models.CharField('User bio', max_length=256, blank=True, null=True)
    confirmation_code = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(10000), MaxValueValidator(99999)]
    )
    email = models.EmailField('E-mail', blank=False)

    class Meta:
        ordering = ('id',)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR

    @property
    def is_user(self):
        return self.role == ROLE_USER
