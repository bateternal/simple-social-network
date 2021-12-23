from chat.models import UserInformations, Conversations
from chat.views import notfound
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def allconversations(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        objects = Conversations.objects.filter(
            user=request.user).order_by('-create_date')
        data = []
        for obj in objects:
            user = UserInformations.objects.get(owner=obj.target)
            data.append(
                {"username": user.username, "pic": user.profile_picture,
                 "date_time": obj.date_time, "text": obj.text, "seen": obj.seen})

        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception:
        return notfound(request)
