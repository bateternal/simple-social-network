from chat.models import UserInformations
from chat.views import notfound
from django.shortcuts import render
from django.http import HttpResponseRedirect


def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        user = UserInformations.objects.get(owner=request.user)
        return render(request, "home.html", 
                      {"pic": user.profile_picture,
                       "firstname": user.firstname,
                       "lastname": user.lastname, "bio": user.bio})
    except Exception:
        return notfound(request)
