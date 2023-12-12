from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializers(serializers.ModelSerializer):
    

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializers(serializers.ModelSerializer):
    

    class Meta:
        model = Genre
        fields = '__all__'




class TitleSerializers(serializers.ModelSerializer):
    

    class Meta:
        model = Title
        fields = '__all__'