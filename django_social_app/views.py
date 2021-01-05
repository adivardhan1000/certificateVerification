from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
  return render(request, 'login.html')


def welcome(request):
  return render(request, 'welcome.html')

def check(request):
  return render(request, 'check.html')

def checking(request):
  return render(request, 'checking.html')

@login_required
def home(request):
  return render(request, 'afterLogin.html')

def institutelogin(request):
  return render(request, 'institutelogin.html')

def institutelogincheck(request):
  return render(request, 'institutelogin.html')
