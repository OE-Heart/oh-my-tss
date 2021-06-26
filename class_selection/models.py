from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from class_schedule.models import ClassHasRoom
from info_mgt.models import Campus, Class, Teacher, Student, Course
from django.contrib.auth.models import User
# from django.contrib import admin
import datetime


class StuHasClass(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)


class sel_time(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    type = models.IntegerField()
