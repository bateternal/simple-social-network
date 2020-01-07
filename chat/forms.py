# -*- coding: utf-8 -*-
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='username', 
                    widget=forms.TextInput(attrs={'placeholder': 'username'}))
	password = forms.CharField(label='password', 
                    widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'input-xlarge'})
		self.fields['password'].widget.attrs.update({'class': 'input-xlarge'})