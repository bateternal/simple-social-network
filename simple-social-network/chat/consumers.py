from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from .models import Messages ,Conversations
from time import time
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.channel_name + "\n\n\n\n")
        data = self.scope['url_route']['kwargs']['room_name']
        self.room_name =data.split('-')[0]
        async_to_sync(self.channel_layer.group_add)(
            data.split('-')[1],
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['message']
        sender = text_data_json['sender']
        target = text_data_json['target']
        date = text_data_json['date']
        message = Messages()
        message.sender = User.objects.get(username=sender)
        message.target = User.objects.get(username=target)
        message.timestamp = time()
        message.text = text
        message.date = date
        message.save()
        obj1, created = Conversations.objects.get_or_create(user=message.sender,target=message.target)
        obj1.text = text
        obj1.date = date
        obj1.seeing = True
        obj1.save()
        obj2, created = Conversations.objects.get_or_create(target=message.sender,user=message.target)
        obj2.text = text
        obj2.date = date
        obj2.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': text,
                'date' : date,
                'pk' : message.id
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'date' : event['date'],
            'pk' :event['pk']

        }))