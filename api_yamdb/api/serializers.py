from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Titles, Reviews, Comments
from statistics import mean


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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = '__all__'
    
    def get_rating(self, obj):
        scores = Reviews.objects.values('score')
        rating = 0
        if scores:
            for score in scores:    # scores список словарей 
                for key, value in score:  
                    rating = rating + value
                return rating
            average_score = round(mean(rating))
        else:
            average_score = 0
        
        return average_score


        


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
    
    def create(self, validated_data):
        review = Reviews.objects.all(author=self.request.user)
        if not review:
            return Reviews.objects.create(**validated_data)
        raise serializers.ValidationError(
            'Пользователь может оставить только один отзыв на произведение.'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('author',)
