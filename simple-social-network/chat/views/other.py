from django.http import HttpResponseRedirect


def other(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    return HttpResponseRedirect('/landing')
