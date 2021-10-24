from django.shortcuts import render
from chat.models import UserInformations, ConfirmToken
from chat.views import notfound
from .forms import LoginForm, RegisterForm
from .tools import ConfirmTool
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/landing")
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST or None)
            register_form = RegisterForm(request.POST or None)
            
            if login_form.is_valid():
                username = login_form.cleaned_data['lusername']
                password = login_form.cleaned_data['lpassword']
                user = authenticate(
                    request, username=username, password=password)
            
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/landing")
                else:
                    return render(request, 'login.html', {
                        'login': LoginForm(), "register": RegisterForm(),
                        "incorrect": True})
            
            elif register_form.is_valid():
                
                name = register_form.cleaned_data['name']
                lastname = register_form.cleaned_data.get('lastname', None)
                username = register_form.cleaned_data['username']
                email = register_form.cleaned_data['email']
                
                user_informations = UserInformations()
                user_informations.firstname = name
                user_informations.lastname = lastname
                user_informations.username = username
                user_informations.email = email
                user_informations.save()
                
                confirm_token = ConfirmToken()
                confirm_token.token = ConfirmTool.generateConfirmToken()
                confirm_token.user = user_informations
                confirm_token.save()

                return HttpResponseRedirect(
                    "/confirm/%s" % confirm_token.token)

        return render(request, 'login.html', {
            'login': LoginForm(), "register": RegisterForm()})
    except Exception:
        return notfound(request)
