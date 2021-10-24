from chat.models import UserInformations
from chat.views import notfound
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


def chat(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        informations = UserInformations.objects.get(
            owner=User.objects.get(username=username))
        return render(request, "chat.html",
                      {"room_name": username, "me": request.user.username,
                       "name": informations.firstname,
                       "pic": informations.profile_picture})
    except Exception:
        return notfound(request)
