from django.contrib.auth.models import User
from chat.models import Messages, Conversations
from chat.views import notfound
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def sync_messages(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    try:
        data = json.loads(str(request.body, 'utf-8'))
        target = User.objects.get(username=data['target'])
        messages = []
        user = User.objects.get(username=data['sender'])
        # target, _, messages, user = User.objects.get(
        #     username=data['target']), data.get('index', 0), [], User.objects.get(username=data['sender'])
        sender_id = user.id
        target_id = target.id
        query = '''select * from message where 
        ("target_id"=%i and "sender_id"=%i) or 
        ("sender_id"=%i and "target_id"=%i) 
        order by id desc limit 10;
        ''' % (sender_id, target_id, sender_id, target_id)
        query = query.replace("\n", "")
        objects = Messages.objects.raw(query)

        messages = [
            [
                {"text": obj.text, "date": obj.date, "pk": obj.id},
                "out" if obj.sender == user else "in"
            ] for obj in objects]
        Conversations.objects.filter(
            user=request.user, target=target).update(seeing=True)

        return HttpResponse(
            json.dumps(messages[::-1]), content_type="application/json")
    except Exception:
        return notfound(request)
