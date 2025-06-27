from django.contrib import admin
from .models import Book, BookIssue, BookHold, Fine, BookReturnRequest

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_name', 'book_author', 'no_of_copies_available','damaged')
    search_fields = ('book_name', 'book_author')
    # list_filter = ('no_of_copies_available','book_author','damaged')


@admin.register(BookHold)
class BookHoldAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'timestamp')
    search_fields = ('student__user__username', 'book__book_name')
    list_filter = ('book',)
    autocomplete_fields = ['student', 'book']

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('student', 'reason', 'amount', 'created_at')
    search_fields = ('student__user__username', 'reason')
    list_filter = ('reason',)
    autocomplete_fields = ['student']

from django.utils import timezone
from datetime import timedelta

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'issue_date', 'return_date', 'is_renewed', 'is_returned')
    list_filter = ('is_renewed', 'is_returned')
    search_fields = ('student__user__username', 'book__book_name')
    actions = ['extend_return_by_2_weeks', 'mark_as_returned', 'revert_return']
    autocomplete_fields = ['student', 'book']

    

    @admin.action(description='Extend return date by 14 days')
    def extend_return_by_2_weeks(self, request, queryset):
        updated = 0
        for issue in queryset.filter(is_returned=False):
            issue.return_date += timedelta(days=14)
            issue.is_renewed = True
            issue.save()
            updated += 1
        self.message_user(request, f"Extended return date for {updated} book(s).")

    @admin.action(description='Mark selected issues as returned')
    def mark_as_returned(self, request, queryset):
        updated = 0
        for issue in queryset.filter(is_returned=False):
            issue.is_returned = True
            issue.returned_on = timezone.now().date()
            issue.book.no_of_copies_available += 1
            issue.book.save()
            issue.save()
            updated += 1
        self.message_user(request, f"Marked {updated} book(s) as returned.")

    @admin.action(description='Revert return (mark as not returned)')
    def revert_return(self, request, queryset):
        updated = 0
        for issue in queryset.filter(is_returned=True):
            issue.is_returned = False
            issue.returned_on = None
            issue.save()
            updated += 1
        self.message_user(request, f"Reverted return for {updated} book(s).")


@admin.register(BookReturnRequest)
class BookReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('issue', 'requested_on', 'approved')
    list_filter = ('approved',)
    search_fields = ('issue__student__user__username', 'issue__book__book_name')
