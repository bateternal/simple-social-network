from django.db import models
from django.contrib.auth.models import User
from enum import Enum


class UserInformations(models.Model):
    class UserType(Enum):

        STUDENT = "STUDENT"
        TEACHER = "TEACHER"

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='owner', null=True, db_index=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.CharField(max_length=40, unique=True)
    profile_picture = models.CharField(max_length=100, null=True)
    bio = models.CharField(max_length=200, default='')
    verified = models.BooleanField(default=False)
    is_ban = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=255, choices=UserType.choices(),
        null=True, default=UserType.STUDENT)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = u'user_information'
