from chat.models import Posts
from chat.views import notfound
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def get_posts(request, username=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("")
    try:
        data = []
        posts = Posts.objects.filter(
            owner=(username and 
                   User.objects.get(username=username) or
                   request.user)
            )
        for post in posts:
            payload = {}
            if post.file:
                payload["is_file"] = True
                payload["file"] = post.file
            payload["title"] = post.title
            payload["content"] = post.content or ""
            payload["pk"] = post.pk
            data.append(payload)
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception:
        return notfound(request)
