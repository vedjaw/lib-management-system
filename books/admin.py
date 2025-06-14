from django.contrib import admin
from .models import Book, BookIssue, BookHold

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_name', 'book_author', 'no_of_copies_available')
    search_fields = ('book_name', 'book_author')
    list_filter = ('no_of_copies_available',)

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issue_date', 'return_date', 'is_renewed', 'is_returned')
    list_filter = ('is_renewed', 'is_returned')
    search_fields = ('student__user__username', 'book__book_name')

@admin.register(BookHold)
class BookHoldAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'timestamp')
    search_fields = ('student__user__username', 'book__book_name')
