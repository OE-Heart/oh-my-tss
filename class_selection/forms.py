from django import forms
from material import *


class Department(forms.Form):
    id = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)


class Major(forms.Form):
    id = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)


class Course(forms.Form):
    name = forms.CharField(max_length=20)
    credit = forms.FloatField()
    capacity = forms.IntegerField()
    duration = forms.CharField(max_length=15)
