from django.shortcuts import render

# Create your views here.

def index(req):
  return render(req, 'info_mgt.html', {'test_param': 'TEST PARAM'})