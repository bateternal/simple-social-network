from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
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
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))