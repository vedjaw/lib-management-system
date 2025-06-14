import csv

with open("students_100.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["username", "email", "password"])  # header

    for i in range(1, 101):
        uname = f"student{i:03}"
        email = f"{uname}@gmail.com"
        password = uname
        writer.writerow([uname, email, password])

print("✅ students_100.csv created successfully.")
