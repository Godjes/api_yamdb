from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Модель администратора для Title."""
    list_display = ('pk', 'name', 'year', 'description',
                    'category')
    search_fields = ('name',)
    list_filter = ('genre',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Модель администратора для Genre."""
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Модель администратора для Category."""
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    """Модель администратора для Review."""
    list_display = ('pk', 'author', 'title',
                    'text', 'score', 'pub_date')
    search_fields = ('author',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Модель администратора для Comments."""
    list_display = ('pk', 'author', 'review',
                    'text', 'pub_date')
    search_fields = ('author',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'
