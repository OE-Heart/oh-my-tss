from django.shortcuts import render
from .models import User


def login(request):
    pass
    '''
    username = request.GET.get('username')
    user_set = set(User.objects.filter(username__contains=username))
    if len(user_set) != 1:
        request.user.groups.
    '''


# Create your views here.
