from chat.views import notfound
from chat.models import Posts
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def delete_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    data = json.loads(str(request.body, 'utf-8'))
    try:
        Posts.objects.get(owner=request.user, pk=data["pk"]).delete()
        return HttpResponse(json.dumps({'errorcode': 0, 'success': True}))
    except Exception:
        return notfound(request)
