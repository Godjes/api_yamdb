from rest_framework import viewsets, mixins
from reviews.models import Category, Genre, Title, Reviews, Comments
from .serializers import (ReviewSerializer, CommentSerializer,
                         TitleSerializers, GenreSerializers,
                         CategorySerializers)


class CRDListViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass

class GenreViewSet(viewsets.ModelViewSet):
    pass

class TitleViewSet(viewsets.ModelViewSet):
    pass

class ReviewViewSet(CRDListViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(CRDListViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

