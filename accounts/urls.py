from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.login_redirect_view, name='login-redirect'),
    path('login/', views.login_view, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('prof/dashboard/', views.prof_dashboard, name='prof-dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('create-prof/', views.create_prof_user, name='create_prof_user'),
    path('create-student/', views.create_student_user, name='create_student_user'),
    
]