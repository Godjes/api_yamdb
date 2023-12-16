from rest_framework import permissions

from users.models import User


# по идее должен стать базовым пермишенов в settings.py
# class IsEmailVerifiedOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return bool(
#             request.method in permissions.SAFE_METHODS
#             or request.user
#             and request.user.is_authenticated
#             and request.user.is_email_verified
#         )


# для отзывов и комментариев
class IsAuthorOrAdminOrModOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
            or request.user.is_staff
        )


# для произведений, жанров и категорий
class IsAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_staff
        )


# для пользователей: дописать
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
            or request.user.is_staff
        )