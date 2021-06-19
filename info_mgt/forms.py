from django import forms
from django.contrib.auth.models import User
from material import *
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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
