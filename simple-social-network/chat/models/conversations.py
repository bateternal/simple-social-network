from django.db import models
from django.contrib.auth.models import User


class Conversations(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userowner")
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="targetchat")
    text = models.TextField(null=True)
    date = models.CharField(max_length=20, null=True)
    create = models.DateTimeField(auto_now_add=True)
    seeing = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'target',)
        indexes = [
            models.Index(fields=['user', 'target', 'create', ]),
        ]
