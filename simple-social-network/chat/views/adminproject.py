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


def raw_data(request, model):
    pass


def single_data(request, model, pk):
    pass


def delete_data(request, model, pk):
    pass


def admin_report(request, level):
    pass


def main_page(request, level):
    pass
