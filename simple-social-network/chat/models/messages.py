from django.db import models
from django.contrib.auth.models import User


class Messages(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender", db_index=True)
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="target", db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)
    timestamp = models.CharField(max_length=20)
    text = models.TextField(null=True)
    date_time = models.CharField(max_length=20, null=True)
    seen = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'target', 'timestamp', ]),
        ]

        db_table = u'message'
