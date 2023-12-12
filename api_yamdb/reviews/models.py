from django.db import models


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
    year = models.DateField()
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


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass
