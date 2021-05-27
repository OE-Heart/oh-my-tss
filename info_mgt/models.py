from django.db import models


class User(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    ADMIN = 'A'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    ]

    zju_id = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=STUDENT)
    hashed_password = models.CharField(max_length=30)
    token = models.CharField(max_length=30)
    last_login = models.DateTimeField()
    # avatar = models.ImageField()


class Course(models.Model):
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

    name = models.CharField(max_length=20)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    credit = models.FloatField()
    major = models.CharField(max_length=15)
    year = models.IntegerField()
    term = models.CharField(max_length=2, choices=TERM_CHOICES)
    capacity = models.IntegerField()
    duration = models.CharField(max_length=15)  # in format like "2 3 3", separated by a space


'''
class Course(models.Model):
    _class = models.ForeignKey(Class, on_delete=models.CASCADE)
    day = models.IntegerField()  # from 1 to 7
    start_at = models.IntegerField()  # 开始于第几节
    duration = models.IntegerField()  # 以节为单位
    # room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # campus is a foreign key of room, will not exist here

'''
