from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Titles, Reviews, Comments
from api.filters import TitleFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Avg
from api.serializers import (
    CategorySerializers, GenreSerializers, TitleSerializers,
    TitleDetailSerializers, ReviewSerializer, CommentSerializer
)

from users.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrModOrReadOnly

class PatchAPIViewReview(APIView):

    def patch(self, request):

        review = get_object_or_404(Reviews, author=self.request.user,
                                   title=Titles.objects.get(pk=self.kwargs.get('title_id')))
        if request.method == 'PATCH':
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class PatchAPIViewComment(APIView):

    def patch(self, request):

        comment = get_object_or_404(Comments, author=self.request.user,
                                   review=Reviews.objects.get(pk=self.kwargs.get('review_id')))
        if request.method == 'PATCH':
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class PatchAPIViewTitles(APIView):

    def patch(self, request):

        title = get_object_or_404(Titles.objects.get(pk=self.kwargs.get('title_id')))
        if request.method == 'PATCH':
            serializer = TitleDetailSerializers(title, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(MixinViewSet,
                   PatchAPIViewTitles):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleDetailSerializers
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    queryset = Titles.objects.annotate(
        rating=Avg('review__score')
    ).order_by('id')

    def get_serializer_class(self):
        if self.action in ('list', 'retrive'):
            return TitleDetailSerializers
        return TitleSerializers


class ReviewViewSet(CRDListViewSet, PatchAPIViewReview):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)

    def get_title(self):
        """Находим нужное произведение."""
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Выводим список отзывов отдельного произведения."""
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_title())


class CommentViewSet(CRDListViewSet, PatchAPIViewComment):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)

    def get_review(self):
        """Находим нужный отзыв."""
        return get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Выводим все комментарии к отзыву."""
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())

