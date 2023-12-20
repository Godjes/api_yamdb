from django import forms
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError

from users.models import User


class AuthenticationForm(forms.Form):
    """Класс представляет форму аутентификации пользователя."""
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def authenticate(self, username=None):
        """
            Метод аутентификации пользователя.
            Принимает параметр username,
            значение которого по умолчанию равно None.
            Пытается найти пользователя с заданным именем
            пользователя и возвращает его.
            Если пользователь не существует, возвращает None.
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def clean(self):
        """
            Метод проверки очищенных данных формы.
            Получает значение username из очищенных данных.
            Если значение username не равно None,
            авторизует пользователя.
            Если пользователь не найден, вызывает ValidationError
            с сообщением "Пользователь с таким именем
            пользователя не существует".
        """
        username = self.cleaned_data.get('username')
        if username is not None:
            self.user_cache = self.authenticate(username=username)
            if self.user_cache is None:
                raise ValidationError(
                    'User with this username does not exist.'
                )
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
            Метод подтверждения разрешения на вход для пользователя.
        """
        if not user.is_active:
            raise ValidationError(
                'This user is inactive.'
            )
        if not user.is_staff:
            raise ValidationError(
                'This user is not a member of staff.'
            )

    def get_user(self):
        return self.user_cache
