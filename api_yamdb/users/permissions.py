from rest_framework import permissions

from users import User


# для отзывов и комментариев
class IsAuthorOrAdminOrModOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.ADMIN
            or request.user.role == User.MODERATOR
            or request.user.is_superuser
        )


# для произведений, жанров и категорий
class IsAuthorOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.ADMIN
            or request.user.is_superuser
        )

# для пользователей: дописать
