from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Titles(models.Model):
    ...


class Reviews(models.Model):
    author = models.IntegerField() #пока не определена юзермодель
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    title = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    score = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(10)],
                                        related_name='review'
    )
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

