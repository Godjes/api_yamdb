from django.db import models
import datetime as dt
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование Жанра'
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование'
    )
    year = models.IntegerField(db_index=True)
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='категория',
        blank=True,
        null=True,
        verbose_name='категория'

    )

    def __str__(self):
        return self.name
    
    def validate(year):
        if dt.datetime.now().year <= year:
            raise ValidationError(
                'Этот год еще не наступил!'
            )
        return year


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Reviews(models.Model):
    author = models.IntegerField() #пока не определена юзермодель
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    title = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    score = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(10)])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    author = models.IntegerField() #пока не определена юзермодель
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text

