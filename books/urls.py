from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_books, name='search-books'),
    path('renew/<int:issue_id>/', views.renew_book, name='renew-book'),
    path('issue/<int:book_id>/', views.issue_book, name='issue-book'),
    path('hold/<int:book_id>/', views.hold_book, name='hold-book'),
    path('unhold/<int:book_id>/', views.unhold_book, name='unhold-book'),
    path('add-fine/<int:student_id>/', views.add_fine, name='add-fine'),
    path('delete-fine/<int:fine_id>/', views.delete_fine, name='delete-fine'),
    path('request-return/<int:issue_id>/', views.request_return, name='request-return'),
    path('approve-return/<int:issue_id>/', views.approve_return, name='approve-return'),
    path('view-students/', views.view_student_users, name='view-student-users'),
    path('view-books/', views.view_books, name='view-books'),
    path('view-issued-books/', views.view_issued_books, name='view-issued-books'),
    path('<str:book_id>/', views.book_detail, name='book-detail'),
]
