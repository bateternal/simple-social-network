from chat.models import Messages
from chat.views import notfound
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from time import time


@csrf_exempt
def add_message(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:    
        data = json.loads(str(request.body, 'utf-8'))
        if request.user.username == data['sender']:
            message = Messages()
            message.sender = User.objects.get(username=data['sender'])
            message.target = User.objects.get(username=data['target'])
            message.timestamp = time()
            message.text = data['text']
            message.date_time = data['date_time']
            message.save()
            return HttpResponse(json.dumps({'errorcode': 0, 'success': True}))
    except Exception:
        return notfound(request)
