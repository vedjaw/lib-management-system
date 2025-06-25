from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from accounts.models import StudentProfile
from .models import CustomUser, StudentProfile
from books.models import BookIssue
from books.models import Book
from django.db.models import Q
from django.db.models import Sum



def is_prof(user):
    return user.is_authenticated and user.is_prof


@login_required
@user_passes_test(is_prof)
# def prof_dashboard(request):
#     students = StudentProfile.objects.all()
#     return render(request, 'accounts/prof_dashboard.html', {
#         'students': students
#     })
# def prof_dashboard(request):
#     query = request.GET.get('q')
#     students = []

#     if query:
#         students = StudentProfile.objects.filter(
#             Q(user__username__icontains=query) |
#             Q(user__email__icontains=query)
#         ).distinct()

#     context = {
#         'students': students,
#         'query': query,
#     }
#     return render(request, 'accounts/prof_dashboard.html', context)

# def prof_dashboard(request):
#     query = request.GET.get('q')
#     students = []

#     if query:
#         students = StudentProfile.objects.filter(
#             Q(user__username__icontains=query) |
#             Q(user__email__icontains=query)
#         ).distinct()

#         for student in students:
#             student.current_issues = student.bookissue_set.filter(is_returned=False)
#             student.returned_issues = student.bookissue_set.filter(is_returned=True)

#     context = {
#         'students': students,
#         'query': query,
#     }
#     return render(request, 'accounts/prof_dashboard.html', context)

# def prof_dashboard(request):
#     query = request.GET.get('q')
#     students = []

#     if query:
#         students = StudentProfile.objects.filter(
#             Q(user__username__icontains=query) |
#             Q(user__email__icontains=query)
#         ).distinct()

#         for student in students:
#             student.current_issues = student.bookissue_set.filter(is_returned=False)
#             student.returned_issues = student.bookissue_set.filter(is_returned=True)
#             student.fines = Fine.objects.filter(student=student)

#     context = {
#         'students': students,
#         'query': query,
#     }
#     return render(request, 'accounts/prof_dashboard.html', context)

def prof_dashboard(request):
    query = request.GET.get('q')
    students = []

    if query:
        students = StudentProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query)
        ).distinct()

        for student in students:
            student.current_issues = student.bookissue_set.filter(is_returned=False)
            student.returned_issues = student.bookissue_set.filter(is_returned=True)
            student.fines = Fine.objects.filter(student=student)


    pending_returns = BookIssue.objects.filter(return_requested=True, is_returned=False)

    context = {
        'students': students,
        'query': query,
        'pending_returns': pending_returns,  
    }
    return render(request, 'accounts/prof_dashboard.html', context)



# @login_required
# def student_dashboard(request):
#     student = request.user.studentprofile
#     issued_books = BookIssue.objects.filter(student=student, is_returned=False)
#     issued_book_ids = issued_books.values_list('book_id', flat=True)

#     query = request.GET.get('q', '')
#     matching_books = Book.objects.filter(
#         Q(book_name__icontains=query) | Q(book_author__icontains=query)
#     ) if query else []

#     return render(request, 'accounts/student_dashboard.html', {
#         'issued_books': issued_books,
#         'issued_book_ids': issued_book_ids,
#         'query': query,
#         'matching_books': matching_books,
#     })

from books.models import BookHold,Fine  # Make sure this is imported


# @login_required
# def student_dashboard(request):
#     student = request.user.studentprofile

#     issued_books = BookIssue.objects.filter(student=student, is_returned=False)
#     issued_book_ids = issued_books.values_list('book_id', flat=True)

#     held_books = BookHold.objects.filter(student=student)
#     held_book_ids = held_books.values_list('book_id', flat=True)

#     query = request.GET.get('q', '')
#     matching_books = Book.objects.filter(
#         Q(book_name__icontains=query) | Q(book_author__icontains=query)
#     ) if query else []

#     return render(request, 'accounts/student_dashboard.html', {
#         'issued_books': issued_books,
#         'issued_book_ids': issued_book_ids,
#         'held_books': held_books,
#         'held_book_ids': held_book_ids,
#         'query': query,
#         'matching_books': matching_books,
#     })

@login_required
def student_dashboard(request):
    student = request.user.studentprofile

    issued_books = BookIssue.objects.filter(student=student, is_returned=False)
    issued_book_ids = issued_books.values_list('book_id', flat=True)

    held_books = BookHold.objects.filter(student=student)
    held_book_ids = held_books.values_list('book_id', flat=True)

    # Fine logic
    fines = Fine.objects.filter(student=student)
    total_fine = fines.aggregate(Sum('amount'))['amount__sum'] or 0

    query = request.GET.get('q', '')
    matching_books = Book.objects.filter(
        Q(book_name__icontains=query) | Q(book_author__icontains=query)
    ) if query else []

    return render(request, 'accounts/student_dashboard.html', {
        'issued_books': issued_books,
        'issued_book_ids': issued_book_ids,
        'held_books': held_books,
        'held_book_ids': held_book_ids,
        'fines': fines,
        'total_fine': total_fine,
        'query': query,
        'matching_books': matching_books,
    })

    
def login_redirect_view(request):
    if request.user.is_authenticated:
        if request.user.is_prof:
            return redirect('prof-dashboard')
        elif request.user.is_student:
            return redirect('student-dashboard')
    return redirect('login')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return render(request, "accounts/login.html")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            if (user_type == "prof" and user.is_prof) or (user_type == "student" and user.is_student):
                login(request, user)
                return redirect("prof-dashboard" if user.is_prof else "student-dashboard")
            else:
                messages.error(request, "Incorrect login type selected.")
        else:
            messages.error(request, "Incorrect password.")

    return render(request, "accounts/login.html")


from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegistrationForm


def create_prof_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_prof = True
            user.is_superuser = True
            user.is_staff = True
            user.save()
            messages.success(request, "Prof user created successfully.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/create_prof.html', {'form': form})


def create_student_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, "User with this email already exists.")
                return redirect('create_student_user')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_student = True
            user.save()

            # Only create profile if it doesn't exist
            if not StudentProfile.objects.filter(user=user).exists():
                StudentProfile.objects.create(user=user)

            messages.success(request, "Student user created successfully.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/create_student.html', {'form': form})



