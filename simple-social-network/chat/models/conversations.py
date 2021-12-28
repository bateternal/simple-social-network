from django.db import models
from django.contrib.auth.models import User


class Conversations(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="userowner", db_index=True)
    target = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="targetchat", db_index=True)
    text = models.TextField(null=True)
    date_time = models.CharField(max_length=20, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    block = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'target',)
        indexes = [
            models.Index(fields=['user', 'target', 'create_date', ]),
        ]

        db_table = u'conversation'
