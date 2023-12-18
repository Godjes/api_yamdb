from django.contrib import admin

from .models import Titles, Genre, Reviews, Comments, Category

@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description',
                    'category')
    search_fields = ('name',)
    list_filter = ('genre',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title',
                    'text', 'score', 'pub_date')
    search_fields = ('author',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review',
                    'text', 'pub_date')
    search_fields = ('author',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'