from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
	target = models.ForeignKey(User, on_delete=models.CASCADE,related_name="target")
	create = models.DateTimeField(auto_now_add=True)
	timestamp = models.CharField(max_length=20)
	text = models.TextField(null=True)

	class Meta:
		indexes = [
			models.Index(fields=['sender','target','timestamp',]),
		]