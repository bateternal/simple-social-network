from chat.views import notfound
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def auto_complete(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        data = json.loads(str(request.body, 'utf-8'))
        objects = User.objects.filter(username__startswith=data['username'])
        results = [obj.username for obj in objects[:5]]
    except Exception:
        return notfound(request)
    return HttpResponse(json.dumps(results), content_type="application/json")
