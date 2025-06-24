from django.db import models
from accounts.models import StudentProfile
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    book_id = models.CharField(max_length=20, unique=True)
    book_name = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    no_of_copies_available = models.PositiveIntegerField(default=1)
    damaged = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.book_name  

class BookIssue(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(default=timezone.now() + timedelta(days=14))
    is_renewed = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    return_requested = models.BooleanField(default=False)
    returned_on = models.DateField(null=True, blank=True)

class BookHold(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Fine(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)  
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} — ₹{self.amount} for {self.reason}"
