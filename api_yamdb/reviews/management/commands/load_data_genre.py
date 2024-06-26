from csv import DictReader

from django.core.management import BaseCommand

# Import the model
from reviews.models import Genre

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    """Кастомная команда для загрузки данных из CSV-файлов в БД"""
    help = "Loads data from genre.csv"

    def handle(self, *args, **options):
        if Genre.objects.exists():
            print('genre data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading genre data")
        for row in DictReader(open('./genre.csv', encoding='utf-8')):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()
