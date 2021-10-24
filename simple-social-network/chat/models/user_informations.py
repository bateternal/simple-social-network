from django.db import models
from django.contrib.auth.models import User


class UserInformations(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner', null=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=40, unique=True)
    profile_picture = models.CharField(max_length=100, null=True)
    bio = models.CharField(max_length=200, default='')
    verified = models.BooleanField(default=False)
