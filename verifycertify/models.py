from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class extraProfileData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # firstname = models.CharField(max_length=120)
    # lastname = models.CharField(max_length=120)
    # username = models.CharField(max_length=120)
    # email = models.CharField(max_length=120)
    authLevel = models.CharField(max_length=1, choices=[(1, 'regular user'), (2,'institute user'), (0,'admin user')])
    mobile = models.CharField(max_length=10)
    instituteName = models.CharField(max_length=10)
    idproof = models.FileField(upload_to='media/')
    approved = models.CharField(max_length=1, choices=[(0, 'pending'), (1,'approved'), (2,'rejected')],default=0)
