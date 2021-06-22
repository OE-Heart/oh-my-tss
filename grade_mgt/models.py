from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from info_mgt.models import Student,Course,Class


class CourseResult(models.Model):
    student = models.ManyToManyField(Student)  # 外键
    course = models.ManyToManyField(Course)  # 外键
    Class = models.ManyToManyField(Class)
    class_performance = models.IntegerField(null=True, blank=True)
    exam_result = models.IntegerField(null=True, blank=True)
    final_result = models.IntegerField(null=True, blank=True)
