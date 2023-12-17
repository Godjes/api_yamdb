from csv import DictReader
from django.core.management import BaseCommand

# Import the model
from reviews.models import Comments


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    # Show this when the comments types help
    help = "Loads data from comments.csv"

    def handle(self, *args, **options):
        if Comments.objects.exists():
            print('comments data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading comments data")
        for row in DictReader(open('./comments.csv', encoding='utf-8')):
            comments = Comments(
                id=row['id'],
                text=row['text'],
                pub_date=row['pub_date'],
                author_id=row['author'],
                review_id=row['review_id'],
            )
            comments.save()
