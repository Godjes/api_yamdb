from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Titles, Reviews, Comments
from statistics import mean


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


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

    class Meta:
        model = Titles
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ('author',)
    
    #def validate_author?
    def create(self, validated_data):
        author = self.context['request'].user
        title = self.context.get('view').kwargs.get('title_id')
        review = Reviews.objects.get(author=author, title = title)
        if review:
            raise serializers.ValidationError(
            'Пользователь может оставить только один отзыв на произведение.'
            )
        return Reviews.objects.create(**validated_data)
        


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('author',)
