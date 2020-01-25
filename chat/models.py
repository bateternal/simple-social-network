from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
	target = models.ForeignKey(User, on_delete=models.CASCADE,related_name="target")
	create = models.DateTimeField(auto_now_add=True)
	timestamp = models.CharField(max_length=20)
	text = models.TextField(null=True)
	date = models.CharField(max_length=20,null=True)

	class Meta:
		indexes = [
			models.Index(fields=['sender','target','timestamp',]),
		]

class UserInformations(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner',null=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	username = models.CharField(max_length=20,unique=True)
	email = models.CharField(max_length=40,unique=True)
	profile_picture = models.CharField(max_length=100,null=True)
	bio = models.CharField(max_length=200,default='')
	verified = models.BooleanField(default=False)

class ConfirmToken(models.Model):
	user = models.ForeignKey(UserInformations, on_delete=models.CASCADE,related_name='user')
	token = models.CharField(max_length=100)

class Posts(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='postsowner')
	title = models.CharField(max_length=20)
	content = models.TextField(null=True)
	file = models.CharField(max_length=100,null=True)

	def clean(self):
		if not (self.file or self.content):
			raise ValidationError("You must specify either file or content")
