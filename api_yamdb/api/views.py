from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Titles, Reviews, Comments
from api.filters import TitleFilter
from api.serializers import (
    CategorySerializers, GenreSerializers, TitleSerializers,
    TitleDetailSerializers, ReviewSerializer, CommentSerializer
)

from users.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrModOrReadOnly


class CRDListViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    pass



class MixinViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly)


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleDetailSerializers
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrive'):
            return TitleDetailSerializers
        return TitleSerializers


class ReviewViewSet(CRDListViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)

    def get_title(self):
        """Находим нужное произведение."""
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Выводим список отзывов отдельного произведения."""
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(CRDListViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)

    def get_review(self):
        """Находим нужный отзыв."""
        return get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Выводим все комментарии к отзыву."""
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

