from chat.models import Conversations
from chat.views import notfound
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def see_message(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        data = json.loads(str(request.body, 'utf-8'))
        Conversations.objects.filter(
            user=request.user,
            target=User.objects.get(data['target'])).update(seeing=True)
        return HttpResponse(json.dumps({'errorcode': 0, 'success': True}))
    except Exception:
        return notfound(request)
