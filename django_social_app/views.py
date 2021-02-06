from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import profiledata
#from soc.pipeline.partial import partial


# Create your views here.
def create(request):
    #if request.method == "POST":
    #    return render(request, 'afterLogin.html')
    return render(request, 'create.html')


def welcome(request):
    return render(request, 'welcome.html')


def check(request):
    if request.method == "POST":
        return render(request, 'checking.html')
    return render(request, 'check.html')


# def checking(request):
#  return render(request, 'checking.html')
def getprofiledata(request):
    return render(request,'createCertificates/profile.html')

@login_required
def home(request):
    '''
    checked = 0
    data = []
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        registeredemail = request.POST['registeredemail']
        mobile = request.POST['mobile']
        instname = request.POST['instname']
        idproof = request.POST['']
        new_user = profiledata.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            registeredemail=registeredemail,
            mobile=mobile,
            instname=instname,
            idproof=idproof
        )
        new_user.save()
        print('Profile saved')
        return render(request, 'afterLogin.html')
    print(request.user.last_login)

    if request.user.last_login is None:

        data = [request.user.first_name,request.user.last_name,request.user.email]
        context = {
        }
        context['data'] = data
        return render(request, 'createCertificates/profile.html',context)
    else:
    '''
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
