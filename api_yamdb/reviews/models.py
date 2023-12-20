import datetime as dt

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

User = get_user_model()

MIN_SCORE = 1
MAX_SCORE = 10


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование Жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование'
    )
    year = models.PositiveSmallIntegerField(db_index=True)
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        blank=True,
        null=True,
        verbose_name='категория'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def validate(self, year):
        if dt.datetime.now().year <= year:
            raise ValidationError(
                'Этот год еще не наступил!'
            )


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.text
