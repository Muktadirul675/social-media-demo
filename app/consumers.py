import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.username = self.scope['user'].username
        self.room_group_name =  self.scope["url_route"]["kwargs"]["key"]
        print(self.room_group_name)
        self.accept()
        print('connect')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "welcome_message", "message": f'Welcome, {self.username}'}
        )

    def welcome_message(self,event):
        msg = event['message']
        self.send(json.dumps({
            'type' :'welcome_message',
            'message' : msg,
            'user' : self.username
            }))

    def receive(self, *, text_data):
        message_json = json.loads(text_data)
        message = message_json['message']
        sender = message_json['sender']
        print(f'Message: {message}; Sender: {sender}')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": f'{message}','sender':sender}
        )

    def chat_message(self,event):
        msg = event['message']
        sender = event['sender']
        self.send(json.dumps({
            'type' :'chat_message',
            'message' : msg,
            'sender': sender,
            "user":self.username
            }))


    def disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )