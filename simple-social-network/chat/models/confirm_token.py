from django.db import models
from chat.models import UserInformations


class ConfirmToken(models.Model):
    user = models.ForeignKey(
        UserInformations, on_delete=models.CASCADE, related_name='user')
    token = models.CharField(max_length=100)
