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
    author = SlugRelatedField(slug_field='username',
                            read_only=True,
                            default=serializers.CurrentUserDefault())

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)


    def validate(self, data):
        if self.context.get('request').method == 'POST':
            author = self.context['request'].user
            title = self.context.get('view').kwargs.get('title_id')
            review = Reviews.objects.filter(author=author, title = title)
            if review:
                raise serializers.ValidationError(
                'Пользователь может оставить только один отзыв на произведение.'
                )
        return data
    
    
        


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                            read_only=True,
                            default=serializers.CurrentUserDefault())

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)
