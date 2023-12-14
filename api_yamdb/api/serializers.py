from rest_framework import serializers
from reviews.models import Category, Genre, Titles


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleDetailSerializers(serializers.ModelSerializer):
    genre = GenreSerializers(many=True, read_only=True)
    category = CategorySerializers()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'


class TitleSerializers(TitleDetailSerializers):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
