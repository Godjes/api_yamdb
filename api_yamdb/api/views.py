from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from api.filters import TitleFilter
from api.serializers import (CategorySerializers, CommentSerializer,
                             GenreSerializers, ReviewSerializer,
                             TitleDetailSerializers, TitleSerializers)
from reviews.models import Category, Genre, Reviews, Titles
from users.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrModOrReadOnly


class CRDListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
        Класс для представления CRUD-операций
        (создание, чтение, удаление, список)
        для модели в виде API-эндпоинтов.
    """
    pass


class MixinViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
        Класс, использующий миксины для представления CRUD-операций
        и для работы с списком моделей
    """
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('=name',)
    lookup_field = ('slug')


class CategoryViewSet(MixinViewSet):
    """
        Класс представления, отображающий операции
        со списком объектов категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class GenreViewSet(MixinViewSet):
    """
        Класс представления, отображающий
        операции со списком объектов жанров.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """
        Класс представления, отображающий
        операции со списком объектов произведений.
    """
    queryset = Titles.objects.annotate(
        rating=Avg('review__score')
    ).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleDetailSerializers
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_serializer_class(self):
        """Метод возвращайющий сериалайзер в зависимости от запроса"""
        if self.request.method == 'GET':
            return TitleDetailSerializers
        return TitleSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    """
        Класс представления, отображающий
        операции со списком отзывов.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_title(self):
        """Находим нужное произведение."""
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Выводим список отзывов отдельного произведения."""
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
        Класс представления, отображающий
        операции со списком комментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_review(self):
        """Находим нужный отзыв."""
        return get_object_or_404(
            Reviews, pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Выводим все комментарии к отзыву."""
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())
