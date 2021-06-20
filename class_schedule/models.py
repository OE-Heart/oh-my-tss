from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from info_mgt.models import Campus, Class, Teacher
# from django.contrib import admin
import datetime


class Building(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)


class Classroom(models.Model):
    COMMON_ROOM = 'O'
    GYM_ROOM = 'G'
    COMPUTER_CENTER_ROOM = 'C'
    TYPE_CHOICES = [
        (COMMON_ROOM, 'Common Classroom'),
        (GYM_ROOM, 'Gymnasium'),
        (COMPUTER_CENTER_ROOM, 'Computer Room'),
    ]
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_number = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    capacity = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=COMMON_ROOM)


class ClassHasRoom(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True)
    day = models.IntegerField(default=1, null=True, blank=True, validators=[MaxValueValidator(7), MinValueValidator(1)])
    start_at = models.IntegerField(default=1, null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(13)])
    # 按理说应该限制2节及以上长度的时段只能在1，3，6，7，9，11节开始，只有长度为1节的才是可取1~13，从view里定义限制吧……
    duration = models.IntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(4)])
    # 这个最大值4哪来的？万恶的沟通技巧。
    end_at = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(13)])


class Application(models.Model):
    submit_time = models.DateTimeField(default=datetime.datetime.now)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    reply_time = models.DateTimeField(null=True, blank=True)
    # admin = models.ForeignKey(admin, on_delete=models.SET_NULL)
    is_accepted = models.BooleanField(null=True, blank=True)
    reply = models.TextField(max_length=100, null=True, blank=True)
