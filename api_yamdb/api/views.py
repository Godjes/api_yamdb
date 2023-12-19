from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Titles, Reviews, Comments
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import permissions, status
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
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('=name',)
    lookup_field = ('slug')


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(
        rating=Avg('review__score')
    ).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleDetailSerializers
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleDetailSerializers
        return TitleSerializers


class ReviewViewSet(viewsets.ModelViewSet):
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
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_review(self):
        """Находим нужный отзыв."""
        return get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Выводим все комментарии к отзыву."""
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())

