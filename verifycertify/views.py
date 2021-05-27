import datetime

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from verifycertify.models import extraProfileData, NewEventData
from django.conf import settings
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

CREATE_CERTIFICATE_REGISTER_PAGE = 'createRegister.html'
CREATE_CERTIFICATE_LOGIN_PAGE = 'createLogin.html'


def welcome(request):
    return render(request, 'welcome.html')


def create(request):
    return render(request, 'create.html')


def createLogin(request):
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
                return render(request, CREATE_CERTIFICATE_LOGIN_PAGE, {
                    'error_message': ' Login Failed! Not authorised.', })
        else:
            messages.info(request, 'Invalid')
            return render(request, CREATE_CERTIFICATE_LOGIN_PAGE, {
                'error_message': ' Login Failed! Enter the username and password correctly', })
    else:
        return render(request, CREATE_CERTIFICATE_LOGIN_PAGE, )


def createRegister(request):
    instituteNames = extraProfileData.objects.values_list('instituteName').filter(authLevel=2, approved=1)
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
                return render(request, CREATE_CERTIFICATE_REGISTER_PAGE, {'error_message': 'Username Taken', })
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return render(request, CREATE_CERTIFICATE_REGISTER_PAGE, {'error_message': 'E-Mail Taken', })
            else:
                fs = FileSystemStorage()
                extension = idproof.name.split(".")[-1]
                filename = fs.save(first_name + last_name + "." + extension, idproof)
                uploaded_file_url = fs.url(filename)
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                profile = extraProfileData.objects.create(user=user, authLevel=1, mobile=mobile,
                                                          instituteName=instituteName, idproof=uploaded_file_url)
                profile.save()
                print('User Created')
                return render(request, 'createLogin.html', {'error_message': 'User Created', })
        else:
            print('User not created')
            return render(request, 'createLogin.html', {'error_message': 'Password doesn\'t match', })

    return render(request, CREATE_CERTIFICATE_REGISTER_PAGE, context)


@login_required(login_url='/create/login')
def createDashboard(request):
    # for field in authValue:
    #    print(field)
    # if not request.user.is_authenticated():
    #     return redirect(createLogin())
    if extraProfileData.objects.get(pk=request.user.id).authLevel == 1:
        data = extraProfileData.objects.get(pk=request.user.id)
        context = {
            'data': data
        }
        return render(request, 'createDashboard.html', context)
    else:
        auth.logout(request)
        return redirect(error)
    # print('------------------redirecting--------------')
    # return redirect(createLogin)


@login_required(login_url='/create/login')
def createNewEvent(request):
    context = {}
    if extraProfileData.objects.get(pk=request.user.id).authLevel == 1:
        if request.method == "POST":
            context['error_message'] = 'Event created'
            fs = FileSystemStorage()
            eventName = "".join([i.capitalize() for i in request.POST['eventName'].split(" ")])

            eventDescription = request.POST['eventDescription']
            eventDate = request.POST['eventDate']
            print("--------------", eventDate)
            proof1 = request.FILES['proof1']
            proof1AuthorisedBy = request.POST['proof1AuthorisedBy']
            ##############################################################
            extension = proof1.name.split(".")[-1]
            filename = fs.save(str(request.user.id) + "_" + eventName + "_" + "proof1"+"."+extension, proof1)
            uploaded_file_url1 = fs.url(filename)

            tempDate = eventDate.split("-")
            eventDate = datetime.date(int(tempDate[0]),int(tempDate[1]),int(tempDate[2]))

            if request.POST['proof2']:
                proof2 = request.FILES['proof2']
                proof2AuthorisedBy = request.POST['proof2AuthorisedBy']
                extension = proof2.name.split(".")[-1]
                filename = fs.save(str(request.user.id) + "_" + eventName + "_" + "proof2"+"."+extension, proof2)
                uploaded_file_url2 = fs.url(filename)
            if request.POST['proof3']:
                proof3 = request.FILES['proof3']
                proof3AuthorisedBy = request.POST['proof3AuthorisedBy']
                extension = proof3.name.split(".")[-1]
                filename = fs.save(str(request.user.id) + "_" + eventName + "_" + "proof3"+"."+extension, proof3)
                uploaded_file_url3 = fs.url(filename)
            if request.POST['proof4']:
                proof4 = request.FILES['proof4']
                proof4AuthorisedBy = request.POST['proof4AuthorisedBy']
                extension = proof4.name.split(".")[-1]
                filename = fs.save(str(request.user.id) + "_" + eventName + "_" + "proof4"+"."+extension, proof4)
                uploaded_file_url4 = fs.url(filename)
            if request.POST['proof5']:
                proof5 = request.FILES['proof5']
                proof5AuthorisedBy = request.POST['proof5AuthorisedBy']
                extension = proof5.name.split(".")[-1]
                filename = fs.save(str(request.user.id) + "_" + eventName + "_" + "proof5"+"."+extension, proof5)
                uploaded_file_url5 = fs.url(filename)
            totalParticipants = request.POST['totalParticipants']
            event = NewEventData.objects.create(
                user = request.user,
                eventName=eventName,
                eventDescription=eventDescription,
                date=eventDate,
                proof1=uploaded_file_url1,
                proof1AuthorisedBy=proof1AuthorisedBy,
                proof2 =uploaded_file_url2 if 'proof2' in locals() else "None",
                proof2AuthorisedBy = proof2AuthorisedBy if 'proof2' in locals() else "None",
                proof3=uploaded_file_url3 if 'proof3' in locals() else "None",
                proof3AuthorisedBy=proof3AuthorisedBy if 'proof3' in locals() else "None",
                proof4=uploaded_file_url4 if 'proof4' in locals() else "None",
                proof4AuthorisedBy=proof4AuthorisedBy if 'proof4' in locals() else "None",
                proof5=uploaded_file_url5 if 'proof5' in locals() else "None",
                proof5AuthorisedBy= proof5AuthorisedBy if 'proof5' in locals() else "None",
                totalParticipants = totalParticipants
            )
            event.save()
            return render(request, 'createNewEvent.html', context)
        return render(request, 'createNewEvent.html')
    else:
        auth.logout(request)
        return redirect(error)


@login_required(login_url='/create/login')
def createManageEvent(request):
    if extraProfileData.objects.get(pk=request.user.id).authLevel == 1:
        if request.method == "POST":
            submitValue = request.POST['action']
            operation, eventID = submitValue.split(" ")
            if operation == 'Delete':
                # deleteing file
                tempEventData = NewEventData.objects.get(pk=int(eventID))
                fs = FileSystemStorage()
                filename = str(tempEventData.proof1)
                print(filename)
                filename = filename.split("/")[-1]
                fs.delete(filename)
                # deleting event
                NewEventData.objects.filter(pk=int(eventID)).delete()
                return redirect(createManageEvent)
        context = {}
        allEvents = NewEventData.objects.filter(user_id=request.user.id)
        eventData = []
        for event in allEvents:
            eventData.append([event.id,event.eventName,event.eventDescription,event.date,'Approved' if event.status == 1 else 'Pending'])
        context['data'] = eventData
        return render(request, 'createManageEvent.html', context)
    else:
        auth.logout(request)
        return redirect(error)




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
            return render(request, 'institutelogin.html', {
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
    context = {}
    if extraProfileData.objects.get(pk=request.user.id).authLevel == 2:
        # --->filtering profiles with authlevel 1
        context['data'] = extraProfileData.objects.get(pk=request.user.id)
        print("------------",context['data'].approved)
        return render(request, 'instituteDashboard.html', context)
    else:
        auth.logout(request)
        return redirect(error)


@login_required(login_url='/institute/login')
def instituteManageUser(request):
    if request.META.get('HTTP_REFERER') == "http://localhost:8000/institute/dashboard/" and  extraProfileData.objects.get(pk=request.user.id).authLevel == 2:
        institute_name = extraProfileData.objects.get(user_id=request.user.id)
        institute_name = institute_name.instituteName
        createUser = extraProfileData.objects.filter(authLevel=1, instituteName=institute_name)
        # print(createUser, "++++++++++++++")
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
            # print(operation, userID, "==============")
            if operation == "Approve":
                extraProfileData.objects.filter(pk=userID).update(approved=1)
            elif operation == "Deny":
                extraProfileData.objects.filter(pk=userID).update(approved=2)
            elif operation == "TempDeny":
                extraProfileData.objects.filter(pk=userID).update(approved=0)
            return redirect(instituteDashboard)
        extraData = extraProfileData.objects.get(pk=request.user.id)
        context['authUser'] = extraData
        return render(request, 'instituteManageUsers.html', context)
    else:
        auth.logout(request)
        return redirect(error)

def verify(request):
    if request.method == "POST":
        return render(request, 'checking.html')
    return render(request, 'verify.html')


@login_required(login_url='/admin')
def authenticateInstitute(request):
    if request.user.is_staff:
        # ---> filtering profiles with authlevel 2
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
    else:
        return redirect(welcome)


def error(request):
    return render(request, '404.html')


@login_required(login_url='/')
def profile(request, message):
    if request.method == 'POST':
        if request.POST['action'] == 'delete':
            u = request.user
            u.delete()
            return redirect(welcome)
    return render(request, 'profile.html')

