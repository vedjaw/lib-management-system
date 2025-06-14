from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookIssue, BookHold
from accounts.models import StudentProfile
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from books.models import BookIssue
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from books.models import Book, BookIssue, BookHold
from accounts.models import StudentProfile

def renew_book(request, issue_id):
    issue = get_object_or_404(BookIssue, id=issue_id)

    if not issue.is_renewed and not issue.is_returned:
        issue.is_renewed = True
        issue.return_date += timedelta(days=14)
        issue.save()

    return redirect('student-dashboard')


def search_books(request):
    query = request.GET.get("q", "")
    books = Book.objects.filter(book_name__icontains=query)
    return render(request, "books/search.html", {"books": books, "query": query})

def book_detail(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    is_on_hold = BookHold.objects.filter(book=book).exists()
    return render(request, "books/detail.html", {"book": book, "on_hold": is_on_hold})

def issue_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    student = StudentProfile.objects.get(user=request.user)

    # 1. Enforce max limit
    issued_count = BookIssue.objects.filter(student=student, is_returned=False).count()
    if issued_count >= 7:
        messages.error(request, "You have already issued 7 books.")
        return redirect('student-dashboard')

    # 2. Enforce available copies check
    if book.no_of_copies_available <= 0:
        messages.error(request, "No copies available.")
        return redirect('book-detail', book_id=book_id)

    # 3. Hold queue enforcement: allow only the first student to issue if holds exist
    hold_queue = BookHold.objects.filter(book=book).order_by('timestamp')
    if hold_queue.exists():
        if hold_queue.first().student != student:
            messages.error(request, "You're not first in the hold queue for this book.")
            return redirect('student-dashboard')
        else:
            # Remove the student from hold queue once they issue
            BookHold.objects.filter(book=book, student=student).delete()

    # 4. Issue the book
    BookIssue.objects.create(book=book, student=student)
    book.no_of_copies_available -= 1
    book.save()

    messages.success(request, "Book issued successfully.")
    return redirect('student-dashboard')






def hold_book(request, book_id):
    student = request.user.studentprofile
    book = get_object_or_404(Book, id=book_id)

    existing = BookHold.objects.filter(book=book, student=student)
    if existing.exists():
        messages.info(request, "You're already in the hold queue.")
    else:
        BookHold.objects.create(book=book, student=student)
        messages.success(request, "Book added to hold queue.")

    return redirect('student-dashboard')


from django.utils import timezone

from django.utils import timezone  # make sure this is present

def return_book(request, issue_id):
    issue = get_object_or_404(BookIssue, id=issue_id, is_returned=False)
    
    # ✅ Mark as returned and record date
    issue.is_returned = True
    issue.returned_on = timezone.now().date()
    issue.save()

    # Update book count
    book = issue.book
    book.no_of_copies_available += 1
    book.save()

    # Check hold queue
    hold = BookHold.objects.filter(book=book).order_by('timestamp').first()
    if hold:
        # Auto-issue to the first student in the queue
        BookIssue.objects.create(
            student=hold.student,
            book=book,
            issue_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=14)
        )
        book.no_of_copies_available -= 1
        book.save()
        hold.delete()

    messages.success(request, f"{book.book_name} returned successfully.")
    return redirect('student-dashboard')


# def return_book(request, issue_id):
#     issue = get_object_or_404(BookIssue, id=issue_id, is_returned=False)
#     issue.is_returned = True
#     issue.save()

#     book = issue.book
#     book.no_of_copies_available += 1
#     book.save()

#     # Check hold queue
#     hold = BookHold.objects.filter(book=book).order_by('timestamp').first()
#     if hold:
#         # Auto-issue to the first student in the queue
#         BookIssue.objects.create(
#             student=hold.student,
#             book=book,
#             issue_date=timezone.now().date(),
#             return_date=timezone.now().date() + timedelta(days=14)
#         )
#         book.no_of_copies_available -= 1
#         book.save()

#         # Remove from queue
#         hold.delete()

#     messages.success(request, f"{book.book_name} returned successfully.")
#     return redirect('student-dashboard')

from django.shortcuts import redirect, get_object_or_404
from books.models import BookHold
from django.contrib import messages

def unhold_book(request, book_id):
    hold = get_object_or_404(BookHold, book_id=book_id, student=request.user.studentprofile)
    hold.delete()
    messages.success(request, "Your hold on the book has been removed.")
    return redirect('student-dashboard')

