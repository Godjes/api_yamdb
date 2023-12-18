from csv import DictReader
from django.core.management import BaseCommand

# Import the model
from reviews.models import Titles


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from titles.csv"

    def handle(self, *args, **options):
        if Titles.objects.exists():
            print('titles data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading titles data")
        for row in DictReader(open('./titles.csv', encoding='utf-8')):
            titles = Titles(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category']


            )
            titles.save()
