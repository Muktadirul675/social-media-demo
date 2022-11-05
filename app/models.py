from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
	room_key = models.CharField(max_length=20)
	def __str__(self):
		return f'{self.room_key}'

class RoomMember(models.Model):
	user = models.ForeignKey(User, related_name="user",on_delete=models.CASCADE)
	room = models.ForeignKey(Room,related_name='room',on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.room} {self.user}'

class RoomMessage(models.Model):
	user = models.ForeignKey(RoomMember, related_name="sender",on_delete=models.CASCADE)
	room = models.ForeignKey(Room,related_name='message',on_delete=models.CASCADE)
	message = models.CharField(max_length=10000)
	time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user}'

