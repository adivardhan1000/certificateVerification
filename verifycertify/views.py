from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from verifycertify.models import extraProfileData
from django.conf import settings
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage


# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')


def create(request):
    return render(request, 'create.html')


def createLogin(request):
    # if request.user.is_authenticated():
    #    return redirect('createDashboard')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print('+++++++++++++++', user)
        if user is not None:
            auth.login(request, user)
            authValue = extraProfileData.objects.get(user_id=request.user.id)
            print(authValue.authLevel)
            if authValue.authLevel == 1:
                print('=========================')
                return redirect(createDashboard)
            else:
                return render(request, 'createLogin.html', {
                    'error_message': ' Login Failed! Not authorised.', })
        else:
            messages.info(request, 'Invalid')
            return render(request, 'createLogin.html', {
                'error_message': ' Login Failed! Enter the username and password correctly', })
    else:
        return render(request, 'createLogin.html',)


def createRegister(request):
    instituteNames = extraProfileData.objects.values_list('instituteName').filter(authLevel=2,approved=1)
    print(instituteNames[0][0])
    context = {
        'data': instituteNames,
    }
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        instituteName = request.POST['instituteName']
        mobile = request.POST['mobile']
        idproof = request.FILES['idproof']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return render(request, 'createRegister.html', {'error_message': 'Username Taken', })
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return render(request, 'createRegister.html', {'error_message': 'E-Mail Taken', })
            else:
                fs = FileSystemStorage()
                extension = idproof.name.split(".")[-1]
                filename = fs.save(first_name + last_name + "." + extension, idproof)
                uploaded_file_url = fs.url(filename)
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                profile = extraProfileData.objects.create(user=user, authLevel=1, mobile=mobile,instituteName=instituteName, idproof=uploaded_file_url)
                profile.save()
                print('User Created')
                return render(request, 'createLogin.html', {'error_message': 'User Created', })
        else:
            print('User not created')
            return render(request, 'createLogin.html', {'error_message': 'Password doesn\'t match', })

    return render(request, 'createRegister.html', context)


@login_required(login_url='/create/login')
def createDashboard(request):
    # for field in authValue:
    #    print(field)
    # if not request.user.is_authenticated():
    #     return redirect(createLogin())
    data = extraProfileData.objects.get(pk=request.user.id)
    context ={
        'data': data
    }
    return render(request, 'createDashboard.html', context)
    # print('------------------redirecting--------------')
    # return redirect(createLogin)


def logout(request):
    auth.logout(request)
    return redirect('/')


def instituteLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print('+++++++++++++++', user)
        if user is not None:
            auth.login(request, user)
            details = extraProfileData.objects.get(pk=request.user.id)
            if details.authLevel == 2:
                print('=========================')
                return redirect(instituteDashboard)
            else:
                return redirect(logout)
        else:
            messages.info(request, 'Invalid')
            return render(request, 'institutelogin.html',{
                    'error_message': ' Login Failed! Enter the username and password correctly', })
    else:
        return render(request, 'institutelogin.html')


def instituteRegister(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        instituteName = request.POST['instituteName']
        mobile = request.POST['mobile']
        idproof = request.FILES['idproof']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect(createRegister)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect(instituteRegister)
            else:
                fs = FileSystemStorage()
                extension = idproof.name.split(".")[-1]
                filename = fs.save(first_name + last_name + "." + extension, idproof)
                uploaded_file_url = fs.url(filename)
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                profile = extraProfileData.objects.create(user=user, authLevel=2, mobile=mobile,
                                                          instituteName=instituteName, idproof=uploaded_file_url)
                profile.save()
                print('User Created')
                return redirect(instituteLogin)
        else:
            print('User not created')
        return redirect(instituteRegister)
    else:
        return render(request, 'instituteregister.html')


@login_required(login_url='/institute/login')
def instituteDashboard(request):
    # --->filtering profiles with authlevel 2
    institute_name = extraProfileData.objects.get(user_id=request.user.id)
    institute_name = institute_name.instituteName
    createUser = extraProfileData.objects.filter(authLevel=1, instituteName=institute_name)
    print(createUser, "++++++++++++++")
    createDetails = []
    # --->creating a list of data with primary user data and extra data to pass to html
    for user in createUser:
        # print(user)
        createUserDetails = User.objects.get(id=user.user_id)
        # print(createDetails.first_name)
        createDetails.append(
            [user.user_id, createUserDetails.first_name, createUserDetails.last_name, createUserDetails.email,
             user.mobile, user.idproof, user.approved])
    # print(createDetails)
    context = {'data': createDetails}
    if request.method == "POST":
        submitValue = request.POST['action']
        operation, userID = submitValue.split(" ")
        extraProfileData.objects.update()
        print(operation, userID, "==============")
        if operation == "Approve":
            extraProfileData.objects.filter(pk=userID).update(approved=1)
        elif operation == "Deny":
            extraProfileData.objects.filter(pk=userID).update(approved=2)
        elif operation == "TempDeny":
            extraProfileData.objects.filter(pk=userID).update(approved=0)
        return redirect(instituteDashboard)
    extraData = extraProfileData.objects.get(pk=request.user.id)
    context['authUser']=extraData
    if extraProfileData.objects.get(pk=request.user.id).authLevel == 2:
        return render(request, 'instituteDashboard.html', context)
    else:
        auth.logout(request)
        return redirect(error)


def verify(request):
    if request.method == "POST":
        return render(request, 'checking.html')
    return render(request, 'verify.html')


def authenticateInstitute(request):
    # --->filtering profiles with authlevel 2
    instituteUser = extraProfileData.objects.filter(authLevel=2)
    print(instituteUser, "++++++++++++++")
    instituteDetails = []
    # --->creating a list of data with primary user data and extra data to pass to html
    for user in instituteUser:
        # print(user)
        instituteUserDetails = User.objects.get(id=user.user_id)
        # print(instituteDetails.first_name)
        instituteDetails.append(
            [user.user_id, instituteUserDetails.first_name, instituteUserDetails.last_name, instituteUserDetails.email,
             user.mobile, user.idproof, user.approved])
    # print(instituteDetails)
    context = {'data': instituteDetails}
    if request.method == "POST":
        submitValue = request.POST['action']
        operation, userID = submitValue.split(" ")
        extraProfileData.objects.update()
        print(operation, userID, "==============")
        if operation == "Approve":
            extraProfileData.objects.filter(pk=userID).update(approved=1)
        elif operation == "Deny":
            extraProfileData.objects.filter(pk=userID).update(approved=2)
        elif operation == "TempDeny":
            extraProfileData.objects.filter(pk=userID).update(approved=0)
        return redirect(authenticateInstitute)
    return render(request, 'authenticateInstitute1.html', context)


def error(request):
    return render(request,'404.html')