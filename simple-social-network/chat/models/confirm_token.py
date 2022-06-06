from django.db import models
from chat.models import UserInformations


class ConfirmToken(models.Model):
    user = models.ForeignKey(
        UserInformations, on_delete=models.CASCADE, related_name='user')
    token = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        db_table = u'confirm_token'
