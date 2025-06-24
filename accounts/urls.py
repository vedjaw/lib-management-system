from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_redirect_view, name='login-redirect'),
    path('login/', views.login_view, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('prof/dashboard/', views.prof_dashboard, name='prof-dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('create-prof/', views.create_prof_user, name='create_prof_user'),
    path('create-student/', views.create_student_user, name='create_student_user'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    
]