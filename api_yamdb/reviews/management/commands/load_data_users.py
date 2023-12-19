from csv import DictReader

from django.core.management import BaseCommand

# Import the model
from users.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    """Кастомная команда для загрузки данных из CSV-файлов в БД"""

    help = "Loads data from users.csv"

    def handle(self, *args, **options):
        if User.objects.exists():
            print('users data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading user data")
        for row in DictReader(open('./users.csv', encoding='utf-8')):
            user = User(
                username=row['username'],
                id=row['id'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=['first_name'],
                last_name=['last_name']



            )
            user.save()
