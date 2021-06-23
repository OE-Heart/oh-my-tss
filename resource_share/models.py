from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from info_mgt.models import Student, Course


class Source(models.Model):
    file_path = models.CharField(max_length=256)
    file_size = models.DecimalField(max_digits=19, decimal_places=2)
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)     # 外键
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 外键
    created_at = models.DateField(auto_now_add=True)    # 自动添加上传时间，之后不会再更改
    updated_at = models.DateField(auto_now=True)    # 自动更新修改时间，每次执行操作都会相应的更改


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 外键
    assignment_start = models.DateTimeField()
    assignment_end = models.DateTimeField()
    assignment_intro = models.TextField()
    assignment_ratio = models.IntegerField(null=True, blank=True)  # 不能默认为0，否则不能区分是录入失败还是成绩真的为0


class AssignmentGrade(models.Model):
    student = models.ManyToManyField(Student)  # 外键
    course = models.ManyToManyField(Course)  # 外键
    assignment_path = models.CharField(max_length=256)
    assignment_result = models.IntegerField(null=True, blank=True)