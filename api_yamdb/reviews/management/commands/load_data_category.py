from csv import DictReader

from django.core.management import BaseCommand

# Import the model
from reviews.models import Category

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    """Кастомная команда для загрузки данных из CSV-файлов в БД"""
    help = "Loads data from category.csv"

    def handle(self, *args, **options):
        if Category.objects.exists():
            print('category data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading category data")
        for row in DictReader(open('./category.csv', encoding='utf-8')):
            category = Category(id=row['id'], name=row['name'],
                                slug=row['slug'])
            category.save()
