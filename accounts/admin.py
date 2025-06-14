from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_student', 'is_prof', 'is_staff', 'is_superuser')
    list_filter = ('is_student', 'is_prof', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gmail', 'max_books_allowed')
    search_fields = ('user__username', 'gmail')
