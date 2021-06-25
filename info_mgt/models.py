from django.db import models
from django.contrib.auth.models import User


class Campus(models.Model):
    name = models.CharField(max_length=10)


class Department(models.Model):
    name = models.CharField(max_length=15)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)


class Major(models.Model):
    name = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, null=True, blank=True, on_delete=models.DO_NOTHING)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.DO_NOTHING)


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()


class Course(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    credit = models.FloatField()
    capacity = models.IntegerField()
    duration = models.CharField(max_length=15)  # in format like "2 3 3", separated by a space


class MajorHasCourse(models.Model):
    COMPULSORY = 'C'
    NON_COMPULSORY = 'N'
    COURSE_TYPE_CHOICES = [
        (COMPULSORY, 'compulsory'),
        (NON_COMPULSORY, 'non-compulsory'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=1, choices=COURSE_TYPE_CHOICES, default=NON_COMPULSORY)


class Class(models.Model):
    AUTUMN_WINTER = 'AW'
    SPRING_SUMMER = 'SS'
    SPRING = 'SP'
    SUMMER = 'SU'
    AUTUMN = 'AU'
    WINTER = 'WI'
    SHORT = 'SH'
    TERM_CHOICES = [
        (AUTUMN_WINTER, 'Autumn and winter semester'),
        (SPRING_SUMMER, 'Spring and summer semester'),
        (SPRING, 'Spring term'),
        (SUMMER, 'Summer term'),
        (AUTUMN, 'Autumn term'),
        (WINTER, 'Winter term'),
        (SHORT, 'Short term'),
    ]
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    term = models.CharField(max_length=2, choices=TERM_CHOICES)
    # memberCnt = models.IntegerField(default=0)


'''
class TeacherHasClass(models.Model):
    class = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Class, on_delete=models.CASCADE)
    capacity = models.IntegerField()
'''
