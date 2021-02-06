from django.db import models
from django.contrib.auth.models import User, auth
# Create your models here.
class profiledata(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #first_name =models.CharField(max_length=120)
    #last_name =models.CharField(max_length=120)
    email =models.CharField(max_length=120)
    registeredemail = models.CharField(max_length=120)
    mobile = models.CharField(max_length=10)
    instname =  models.CharField(max_length=10)
    idproof = models.FileField(upload_to='documents/')
    profiledatacomplete = models.BooleanField()
