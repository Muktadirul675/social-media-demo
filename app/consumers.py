import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from . import models 
from django.core import serializers

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope['user'].username
        self.room_group_name =  self.scope["url_route"]["kwargs"]["key"]
        room = None 
        if not models.Room.objects.filter(room_key=self.room_group_name).exists():
            new_room = models.Room(room_key=self.room_group_name)
            room = new_room
            new_room.save()
            print(f'Room {self.room_group_name} created')
        else:
            room = models.Room.objects.get(room_key=self.room_group_name)
            print(f'Room {self.room_group_name} connected')
        #messages = models.Message.objects.filter(room=room)
        #messages = serializers.serialize('json', messages)
        #print(messages)
        self.current_room = room 
        self.connected_user = User.objects.get(username=self.username)
        member = None 
        if models.RoomMember.objects.filter(user=self.connected_user).exists():
            self.room_member = models.RoomMember.objects.get(user=self.connected_user)
            print(f"{self.room_member} signed in")
        else:
            new_room_member = models.RoomMember(user=self.connected_user,room=self.current_room)
            member = new_room_member
            new_room_member.save()
            self.room_member = member 
            print(f'{self.room_member} added')
        self.accept()
        print('connect')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "welcome_message", "message": f'Welcome, {self.username}',}
        )

    def welcome_message(self,event):
        msg = event['message']
        self.send(json.dumps({
            'type' :'welcome_message',
            'message' : msg,
            'user' : self.username,
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
        new_message = models.RoomMessage(user=self.room_member,room=self.current_room,message=msg)
        new_message.save()
        self.send(json.dumps({
            'type' :'chat_message',
            'message' : msg,
            'sender': sender,
            "user":self.username,
            }))


    def disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )