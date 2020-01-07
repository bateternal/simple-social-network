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


class RegisterForm(forms.Form):
	username = forms.CharField(label='username', 
                    widget=forms.TextInput(attrs={'placeholder': 'username'}))
	name = forms.CharField(label='name', 
                    widget=forms.TextInput(attrs={'placeholder': 'name'}))
	lastname = forms.CharField(label='lastname', 
                    widget=forms.TextInput(attrs={'placeholder': 'lastname'}))
	email = forms.CharField(label='email', 
                    widget=forms.TextInput(attrs={'placeholder': 'email'}))
	password = forms.CharField(label='password', 
                    widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'input-xlarge'})
		self.fields['name'].widget.attrs.update({'class': 'input-xlarge'})
		self.fields['lastname'].widget.attrs.update({'class': 'input-xlarge'})
		self.fields['eamil'].widget.attrs.update({'class': 'input-xlarge'})
		self.fields['password'].widget.attrs.update({'class': 'input-xlarge'})
