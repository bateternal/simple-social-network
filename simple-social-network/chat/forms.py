# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    lusername = forms.CharField(
        label='lusername', 
        widget=forms.TextInput(attrs={'placeholder': 'username'}))
    lpassword = forms.CharField(
        label='lpassword', 
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lusername'].widget.attrs.update({'class': 'input-xlarge'})
        self.fields['lpassword'].widget.attrs.update({'class': 'input-xlarge'})


class Test(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'id': 'imageLoader'})


class Confirm(forms.Form):
    file = forms.FileField()
    password = forms.CharField(
        label='password', 
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    bio = forms.CharField(
        label='bio', 
        widget=forms.Textarea(attrs={'placeholder': 'bio'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update(
            {'class': 'file', 'accept': "image/*"})
        self.fields['file'].widget.attrs.update(
            {'id': 'imageLoader'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'rows': "5"})
        self.fields['password'].widget.attrs.update(
            {'id': 'password_form'})        
        self.fields['bio'].widget.attrs.update(
            {'class': 'form-control mb-2 mr-sm-2'})
        self.fields['bio'].widget.attrs.update(
            {'id': 'bio_form'})    


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='username', 
        widget=forms.TextInput(attrs={'placeholder': 'username'}))
    name = forms.CharField(
        label='name', 
        widget=forms.TextInput(attrs={'placeholder': 'first name'}))
    lastname = forms.CharField(
        label='lastname', 
        widget=forms.TextInput(attrs={'placeholder': 'last name'}))
    email = forms.EmailField(
        label='email', 
        widget=forms.TextInput(attrs={'placeholder': 'email'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-xlarge'})
        self.fields['name'].widget.attrs.update({'class': 'input-xlarge'})
        self.fields['lastname'].widget.attrs.update({'class': 'input-xlarge'})
        self.fields['email'].widget.attrs.update({'class': 'input-xlarge'})


class Search(forms.Form):
    username = forms.CharField(
        label='username', 
        widget=forms.TextInput(attrs={'placeholder': 'username'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})


class Upload(forms.Form):
    file = forms.FileField()
    title = forms.CharField(
        label='title', 
        widget=forms.TextInput(attrs={'placeholder': 'title'}),required=False)
    content = forms.CharField(
        label='content', 
        widget=forms.Textarea(attrs={'placeholder': 'content'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update(
            {'class': 'file', 'accept': "image/*"})
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'rows': "5"})
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control mb-2 mr-sm-2'})    
