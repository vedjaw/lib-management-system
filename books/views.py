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

 
    issued_count = BookIssue.objects.filter(student=student, is_returned=False).count()
    if issued_count >= 7:
        messages.error(request, "You have already issued 7 books.")
        return redirect('student-dashboard')

    
    if book.no_of_copies_available <= 0:
        messages.error(request, "No copies available.")
        return redirect('book-detail', book_id=book_id)

    
    hold_queue = BookHold.objects.filter(book=book).order_by('timestamp')
    if hold_queue.exists():
        if hold_queue.first().student != student:
            messages.error(request, "You're not first in the hold queue for this book.")
            return redirect('student-dashboard')
        else:
            
            BookHold.objects.filter(book=book, student=student).delete()

    
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

from django.utils import timezone  

# def return_book(request, issue_id):
#     issue = get_object_or_404(BookIssue, id=issue_id, is_returned=False)
    
    
#     issue.is_returned = True
#     issue.returned_on = timezone.now().date()
#     issue.save()

    
#     book = issue.book
#     book.no_of_copies_available += 1
#     book.save()

   
#     hold = BookHold.objects.filter(book=book).order_by('timestamp').first()
#     if hold:
        
#         BookIssue.objects.create(
#             student=hold.student,
#             book=book,
#             issue_date=timezone.now().date(),
#             return_date=timezone.now().date() + timedelta(days=14)
#         )
#         book.no_of_copies_available -= 1
#         book.save()
#         hold.delete()

#     messages.success(request, f"{book.book_name} returned successfully.")
#     return redirect('student-dashboard')


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


from .models import Fine

# def add_fine(request, student_id):
#     student = get_object_or_404(StudentProfile, id=student_id)

#     if request.method == 'POST':
#         reason = request.POST.get('reason')
#         amount = int(request.POST.get('amount'))
#         Fine.objects.create(student=student, reason=reason, amount=amount)
#         messages.success(request, "Fine levied successfully.")
#         return redirect('prof-dashboard') 

from urllib.parse import urlencode

def add_fine(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        amount = int(request.POST.get('amount'))
        Fine.objects.create(student=student, reason=reason, amount=amount)
        messages.success(request, "Fine levied successfully.")

        # Redirect with search query so it stays on the same page
        query = urlencode({'q': student.user.username})
        return redirect(f'/prof/dashboard/?{query}')



# def delete_fine(request, fine_id):
#     fine = get_object_or_404(Fine, id=fine_id)
#     fine.delete()
#     messages.success(request, "Fine removed.")
#     return redirect('prof-dashboard')


from urllib.parse import urlencode

def delete_fine(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    student_username = fine.student.user.username
    fine.delete()
    messages.success(request, "Fine removed.")

    # Redirect back to the same student
    query = urlencode({'q': student_username})
    return redirect(f'/prof/dashboard/?{query}')

def request_return(request, issue_id):
    issue = get_object_or_404(BookIssue, id=issue_id, student=request.user.studentprofile, is_returned=False)
    issue.return_requested = True
    issue.save()
    messages.success(request, "Return request sent to professor.")
    return redirect('student-dashboard')

# books/views.py
def approve_return(request, issue_id):
    issue = get_object_or_404(BookIssue, id=issue_id, return_requested=True, is_returned=False)
    issue.is_returned = True
    issue.returned_on = timezone.now()
    issue.return_requested = False
    issue.save()

    issue.book.no_of_copies_available += 1
    issue.book.save()

    messages.success(request, "Book return approved.")
    return redirect(f'/prof/dashboard/?q={issue.student.user.username}')


from django.shortcuts import render
from accounts.models import StudentProfile
from .models import Book

def view_student_users(request):
    students = StudentProfile.objects.select_related('user').all()
    return render(request, 'books/view_students.html', {'students': students})

def view_books(request):
    books = Book.objects.all()
    return render(request, 'books/view_books.html', {'books': books})

from .models import BookIssue

def view_issued_books(request):
    issued_books = BookIssue.objects.filter(is_returned=False).select_related('student', 'book', 'student__user')
    return render(request, 'books/view_issued_books.html', {'issued_books': issued_books})
