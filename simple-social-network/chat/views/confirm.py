from chat.models import ConfirmToken
from chat.views import notfound
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import Confirm
from .tools import ConfirmTool
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.contrib.auth import login
import base64


MEDIA_DIRECTORY = os.environ.get('MEDIA_DIRECTORY')


@csrf_exempt
def confirm(request, token):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/landing")
    try:
        confirm_token = get_object_or_404(ConfirmToken, token=token)
        if request.method == 'POST':
            data = json.loads(str(request.body, 'utf-8'))
            password = data['password']
            bio = data['bio']

            path = '/%s/%s.jpg' % (
                os.environ.get('MEDIA_DIRECTORY'),
                ConfirmTool.generateConfirmToken())
            file = data['file']
            
            imgdata = base64.b64decode(file[23:])
            
            with open(path, 'wb') as f:
                f.write(imgdata)
            user_informations = confirm_token.user
            user_informations.bio = bio
            user_informations.owner = User.objects.create_user(
                user_informations.username,
                user_informations.email,
                password)
            user_informations.profile_picture = path
            user_informations.save()
            login(request, user_informations.owner)
            return HttpResponse(json.dumps({"ok": True}))
        return render(request, "confirm.html", {'confirm': Confirm()})
    except Exception:
        return notfound(request)
