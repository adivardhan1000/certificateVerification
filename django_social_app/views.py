from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.
def login(request):
    #if request.method == "POST":
    #    return render(request, 'afterLogin.html')
    return render(request, 'login.html')


def welcome(request):
    return render(request, 'welcome.html')


def check(request):
    if request.method == "POST":
        return render(request, 'checking.html')
    return render(request, 'check.html')


# def checking(request):
#  return render(request, 'checking.html')

@login_required
def home(request):
    return render(request, 'afterLogin.html')

def page_not_found(request,exception):
    return render(request,'404.html')

def internal_server_error(request):
    return render(request,'404.html')

def institutelogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("institutehome.html")
        else:
            messages.info(request, 'Invalid')
            return redirect('institutelogin.html')
    else:
        return render(request, 'institutelogin.html')


def instituteregister(request):
    if request.method == 'POST':
        inst_name = request.POST['inst_name']
        inst_auth = request.POST['inst_auth']
        inst_username = request.POST['inst_username']
        inst_email = request.POST['inst_email']
        inst_number = request.POST['inst_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(inst_username=inst_username).exists():
                messages.info(request, 'Username taken')
                return redirect('inst_register.html')
            elif User.objects.filter(inst_email=inst_email).exists():
                messages.info(request, 'Email taken')
                return redirect('inst_register.html')
            else:
                user = User.objects.create_user(
                    inst_name=inst_name,
                    inst_auth=inst_auth,
                    inst_username=inst_username,
                    inst_email=inst_email,
                    inst_number=inst_number,
                    password=password,
                )
                user.save()
                print('User Created')
                return redirect('institutelogin.html')
        else:
            print('User not created')
        return redirect('/')
    else:
        return render(request, 'instituteregister.html')
