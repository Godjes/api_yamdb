import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class AuthSerializer(serializers.ModelSerializer):
    """Класс, сериализующий данные аутентификации."""
    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'username': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
        }

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Invalid username.'
            )
        elif not re.match(r"^[\w.@+-]+\Z", value):
            raise serializers.ValidationError(
                'Invalid username.'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    """Класс, сериализующий данные токена."""
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }


class ChoiceField(serializers.ChoiceField):
    """Сериализатор для выбора роли"""

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class UsersSerializer(serializers.ModelSerializer):
    """Класс, сериализующий данные пользователей."""
    role = ChoiceField(choices=User.ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'username': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
        }

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Invalid username.'
            )
        elif not re.match(r"^[\w.@+-]+\Z", value):
            raise serializers.ValidationError(
                'Invalid username.'
            )
        return value


class MeSerializer(UsersSerializer):
    """Класс, сериализующий данные текущего пользователя."""
    role = ChoiceField(choices=User.ROLE_CHOICES, required=False,
                       read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'username': {
                'required': False,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'email': {
                'required': False,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
        }
