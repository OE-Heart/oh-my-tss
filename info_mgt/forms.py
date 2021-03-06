from django import forms
from django.contrib.auth.models import User
from material import *
from info_mgt.models import Course, Avatar, Student, Teacher
from oh_my_tss import demo as forms


# class SignupForm(forms.Form):
#     username = forms.CharField(max_length=50)
#     first_name = forms.CharField(max_length=250)
#     last_name = forms.CharField(max_length=250)
#     emails = forms.EmailField(label="Email Address")

#     layout = Layout(
#         'username',
#         Row('first_name', 'last_name'),
#         'emails',
#     )
class SelfInfoForm(forms.Form):
    username = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password_again = forms.CharField(max_length=128, widget=forms.PasswordInput)
    layout = Layout(
        'username',
        Row('last_name', 'first_name'),
        Row('password', 'password_again'),
        'email'
    )

class EditInfoForm(forms.Form):
    username = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    major = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password_again = forms.CharField(max_length=128, widget=forms.PasswordInput)
    layout = Layout(
        'username', 'major',
        Row('last_name', 'first_name'),
        Row('password', 'password_again'),
        'email'
    )
#
# class AvatarForm(SelfInfoForm):
#     class Meta:
#         model = Avatar
#         fields = ['avatar']



class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


# class NewCourseForm(forms.Form):
#     name = forms.CharField(max_length=20)
#     description = forms.CharField(widget=forms.Textarea)
#     credit = forms.FloatField(min_value=0)
#     capacity = forms.IntegerField(min_value=0)
#     duration = forms.CharField(max_length=15)
#
#     layout = Layout('course_name',
#                     'description',
#                     Row('credit', 'capacity', 'duration'))


class CourseEditForm(forms.ModelForm):
    layout = Layout('name',
                    'description',
                    Row('credit', 'capacity', 'duration'))

    class Meta:
        model = Course
        fields = '__all__'


class ClassAddForm(forms.Form):
    course = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    year = forms.IntegerField(min_value=1980)
    choices = [
        ('AW', '????????????'),
        ('SS', '????????????'),
        ('SP', '?????????'),
        ('SU', '?????????'),
        ('AU', '?????????'),
        ('WI', '?????????'),
        ('SH', '?????????'),
    ]
    term = forms.CharField(widget=forms.Select(choices=choices))
    layout = Layout('course',
                    Row('first_name', 'last_name'),
                    Row('year', 'term'))

class AddForm(forms.Form):
    username = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=100)
    major = forms.CharField(max_length=20)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password_again = forms.CharField(max_length=128, widget=forms.PasswordInput)
    choices = [
        ('student', '??????'),
        ('teacher', '??????'),
    ]
    role = forms.CharField(widget=forms.Select(choices=choices))
    layout = Layout(Row('username', 'major', 'role'),
                    Row('password', 'password_again'),
                    Row('last_name', 'first_name'), 'email')


class EditACForm(forms.Form):
    username = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=100)
    major = forms.CharField(max_length=20)

    layout = Layout(Row('username', 'major'),
                    Row('last_name', 'first_name'), 'email')


class Major(forms.ModelForm):

    class Meta:
        models = Student
        fields = ['major',]