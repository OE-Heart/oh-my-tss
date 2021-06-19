from django import forms
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
class SelfInfoForm(forms.Form):
    UserName = forms.CharField(max_length=128, label="姓名")
    UserId = forms.CharField(max_length=11, label="学工号")
    UserDepart = forms.CharField(max_length=20, label="院系")
    UserMajor = forms.CharField(max_length=20, label="专业")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
