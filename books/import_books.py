import csv
from books.models import Book

def import_books_from_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            book_id = row['book_id']
            book_name = row['book_name']
            book_author = row['book_author']
            no_of_copies = int(row['no_of_copies_available'])

            obj, created = Book.objects.get_or_create(
                book_id=book_id,
                defaults={
                    'book_name': book_name,
                    'book_author': book_author,
                    'no_of_copies_available': no_of_copies
                }
            )
            if created:
                count += 1
        print(f"✅ Imported {count} new books.")

# Run the import
import_books_from_csv('books/books_500.csv')
