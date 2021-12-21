from django.http import HttpResponseRedirect
from proxy.views import proxy_view


def other(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    return proxy_view(request, "http://webterminal:80")
