from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Posts(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='postsowner')
    title = models.CharField(max_length=20)
    content = models.TextField(null=True)
    file = models.CharField(max_length=100, null=True)

    def clean(self):
        if not (self.file or self.content):
            raise ValidationError("You must specify either file or content")
