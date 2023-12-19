from csv import DictReader

from django.core.management import BaseCommand

# Import the model
from reviews.models import GenreTitle

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    """Кастомная команда для загрузки данных из CSV-файлов в БД"""
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            print('genre_title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading genre_title data")
        for row in DictReader(open('./genre_title.csv', encoding='utf-8')):
            genre_title = GenreTitle(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            genre_title.save()
