from django.shortcuts import render
from chat.models import UserInformations, Posts
from chat.views import notfound
from .forms import Upload, Confirm
from .tools import ConfirmTool
from django.http import HttpResponseRedirect


def new(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        if request.method == 'POST':
            form = Upload(request.POST, request.FILES)

            if form.is_valid():
                
                title = form.cleaned_data['title']
                content = form.cleaned_data.get('content', None)
                path = 'media/%s' % ConfirmTool.generateConfirmToken()

                file = request.FILES.get('file', None)
                if file is not None:
                    destination = open(path, 'wb+')
                    for chunk in file.chunks():
                        destination.write(chunk)
                    destination.close()
                    path = "/" + path
                else:
                    path = None
                post = Posts()
                post.content = content
                post.title = title
                post.file = path
                post.owner = request.user
                post.save()
                return HttpResponseRedirect("/home")
        user = UserInformations.objects.get(owner=request.user)        
        return render(
            request, 'new.html',
            {
                'upload': Upload(),
                "pic": user.profile_picture,
                "confirm": Confirm()
            }
            )
    except Exception:
        return notfound(request)
