from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class extraProfileData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # firstname = models.CharField(max_length=120)
    # lastname = models.CharField(max_length=120)
    # username = models.CharField(max_length=120)
    # email = models.CharField(max_length=120)
    authLevel = models.IntegerField(max_length=1, choices=[(1, 'regular user'), (2, 'institute user'), (0, 'admin user')])
    mobile = models.CharField(max_length=10)
    instituteName = models.CharField(max_length=10)
    idproof = models.FileField(upload_to='media/')
    approved = models.IntegerField(max_length=1, choices=[(0, 'pending'), (1, 'approved'), (2, 'rejected')], default=0)


class NewEventData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eventName = models.CharField(max_length=20)
    eventDescription = models.CharField(max_length=150)
    date = models.DateField(default=datetime.date.today())
    proof1 = models.FileField(upload_to='media/')
    proof1AuthorisedBy = models.CharField(max_length=25)
    proof2 = models.FileField(upload_to='media/')
    proof2AuthorisedBy = models.CharField(max_length=25)
    proof3 = models.FileField(upload_to='media/')
    proof3AuthorisedBy = models.CharField(max_length=25)
    proof4 = models.FileField(upload_to='media/')
    proof4AuthorisedBy = models.CharField(max_length=25)
    proof5 = models.FileField(upload_to='media/')
    proof5AuthorisedBy = models.CharField(max_length=25)
    totalParticipants = models.IntegerField()
    status = models.IntegerField(choices=[(0, 'pending'), (1, 'approved')], default=0)




