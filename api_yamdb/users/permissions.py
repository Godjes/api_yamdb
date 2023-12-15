from rest_framework import permissions

from users.models import User


# по идее должен стать базовым пермишенов в settings.py
class IsEmailVerifiedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_email_verified
        )


# для отзывов и комментариев
class IsAuthorOrAdminOrModOrReadOnly(IsEmailVerifiedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.ADMIN
            or request.user.role == User.MODERATOR
            or request.user.is_superuser
        )


# для произведений, жанров и категорий
class IsAdminOrReadOnly(IsEmailVerifiedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == User.ADMIN
            or request.user.is_superuser
        )


# для пользователей: дописать
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.role == User.ADMIN
            and request.user.is_email_verified
        )