from django.db import models


class User(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    ADMIN = 'A'
    USER_ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    ]

    zju_id = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=1, choices=USER_ROLE_CHOICES, default=STUDENT)
    hashed_password = models.CharField(max_length=30)
    token = models.CharField(max_length=30)
    last_login = models.DateTimeField()
    # avatar = models.ImageField()


class Course(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    credit = models.FloatField()
    major = models.CharField(max_length=15)
    capacity = models.IntegerField()

