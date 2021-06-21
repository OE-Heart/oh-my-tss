from django import forms
from django.contrib.auth.models import User
from material import *
from info_mgt.models import Course, Avatar
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
class SelfInfoForm(forms.ModelForm):
    layout = Layout(
        'username',
        Row('last_name', 'first_name'),
        'email'
    )

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')
        help_texts = {'username':""}


class AvatarForm(SelfInfoForm):
    class Meta:
        model = Avatar
        fields = ['avatar']



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