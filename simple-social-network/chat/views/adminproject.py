from django.shortcuts import render
from chat.forms import Search
from django.http import HttpResponseRedirect
from proxy.views import proxy_view


def adminproject(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    return render(
        request, "landing.html",
        {
            "search": Search(),
            "user": request.user.username
        }
        )


def shell(request):
    if request.user.is_authenticated:
        return proxy_view(request, "http://webterminal:2100")


def shell80(request):
    if request.user.is_authenticated:
        return proxy_view(request, "http://webterminal:80")
