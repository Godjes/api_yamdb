# Generated by Django 3.2 on 2023-12-19 13:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0004_reviews_unique_review'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
        migrations.RenameModel(
            old_name='Titles',
            new_name='Title',
        ),
    ]
