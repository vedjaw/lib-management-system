from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile

# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'is_student', 'is_prof', 'is_staff', 'is_superuser')
#     list_filter = ('is_student', 'is_prof', 'is_staff')
#     search_fields = ('username', 'email')
class CustomUserAdmin(UserAdmin):
    # model = CustomUser
    list_display = ('username', 'email', 'is_student', 'is_prof', 'is_staff', 'is_superuser')
    list_filter = ('is_student', 'is_prof', 'is_staff', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('is_student', 'is_prof')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('is_student', 'is_prof')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gmail', 'max_books_allowed')
    search_fields = ('user__username', 'gmail')
