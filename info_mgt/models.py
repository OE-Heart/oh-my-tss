from django.db import models


class User(models.Model):
    zju_id = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=1)
    hashed_password = models.CharField(max_length=30)
    token = models.CharField(max_length=30)
    last_login = models.DateTimeField()

    # TODO: add user avatar


'''
class Course(models.Model):
    name
    profession = models.CharField()  # 
'''

# Create your models here.
