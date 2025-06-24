import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()



import csv
from accounts.models import CustomUser, StudentProfile

created_count = 0

with open("students_100.csv", newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:
        username = row["username"]
        email = row["email"]
        password = row["password"]

        if CustomUser.objects.filter(username=username).exists():
            continue

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_student = True
        user.save()

        StudentProfile.objects.create(
            user=user,
            gmail=email,
            max_books_allowed=7
        )

        created_count += 1

print(f"✅ Successfully created {created_count} student users.")
