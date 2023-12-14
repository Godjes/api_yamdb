from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import AdminOrReadOnly
from reviews.models import Category, Genre, Titles
from api.filters import TitleFilter
from api.serializers import (
    CategorySerializers, GenreSerializers, TitleSerializers,
    TitleDetailSerializers
)


class MixinViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrReadOnly)


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = AdminOrReadOnly
    serializer_class = TitleDetailSerializers
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrive'):
            return TitleDetailSerializers
        return TitleSerializers
