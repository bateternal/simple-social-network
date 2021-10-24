from chat.models import UserInformations
from chat.views import notfound, home
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


def profile(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        if request.user.username == username:
            return home(request)
        informations = UserInformations.objects.get(
            owner=User.objects.get(username=username))
        return render(
            request, "profile.html", {
                "username": username, "firstname": informations.firstname,
                "lastname": informations.lastname, "bio": informations.bio,
                "pic": informations.profile_picture})
    except Exception:
        return notfound(request)
