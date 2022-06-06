from django.shortcuts import render
from django.http import HttpResponseRedirect


def conversations(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")    
    return render(request, 'conversations.html', {})
