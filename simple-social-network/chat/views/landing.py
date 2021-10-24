from django.shortcuts import render
from chat.forms import Search
from django.http import HttpResponseRedirect


def landing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    return render(
        request, "landing.html",
        {
            "search": Search(),
            "user": request.user.username
        }
        )
