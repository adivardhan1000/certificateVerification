from django.shortcuts import redirect
from .models import profiledata
#from socia.pipeline.partial import partial
from django_social_app import views
from social_core.pipeline.partial import partial

@partial
def requestprofiledata(strategy, details, user=None, is_new=False, *args, **kwargs):
    print("===============")
    print(details)
    print(type(user))
    print(user)
    #print(user.first_name,"..............")
    #print(user.registeredemail)
    test = 0
    #if user and user.email and test != 0:
    if test == 1:
        return
    #elif is_new and not details.get('email'):
    else:
        registeredemail = strategy.request_data().get("registeredemail")
        #user['registeredemail'] = strategy.request_data().get("registeredemail")
        mobile = strategy.request_data().get("mobile")
        instname = strategy.request_data().get("instname")
        idproof = strategy.request_data().get("idproof")
        #test = 1
        '''
        new_user = profiledata.objects.create(
            registeredemail=registeredemail,
            mobile=mobile,
            instname=instname,
            idproof=idproof
        )
        new_user.save()
        print('Profile saved')
        '''
        #details['registeredemail'] = registeredemail
        print("Details--------------",details)
        if registeredemail:
            print("found data")
            print("data",registeredemail,mobile,instname)
            print("user",user)
            print(".................................")
            if test == 1:
                return  {'user':user}
        else:
            return redirect('getprofiledata')