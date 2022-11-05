from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import unauthenticated, authenticated
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . import models
# Create your views here.

import random
def create_room_key(user1,user2):
	user1_id = user1.id
	user2_id = user2.id
	room_key = f'{user1_id}{user2_id}'
	if user2_id > user1_id:
		room_key = f'{user2_id}{user1_id}'

	return room_key

@authenticated
def room(request, user2_id, key):
	user1 = request.user
	user2 = User.objects.get(pk=user2_id)
	room = None
	if not models.Room.objects.filter(room_key=key).exists():
		new_room = models.Room(room_key=key)
		room = new_room
		new_room.save()
		print(f'Room {key} created from view')
	else:
		room = models.Room.objects.get(room_key=key)
		print(f'Room {key} connected from view')
	messages = list(models.RoomMessage.objects.filter(room=room))
	print(messages)
	cont = {"u1":user1,'u2':user2,'room_key':key, 'room_messages':messages}

	return render(request,'room.html',cont)


@authenticated
def home(request):
	users = list(User.objects.all())
	users.remove(request.user)
	rooms = []
	for i in users:
		room_key = create_room_key(request.user, i)
		obj = {'user':i,'room_key':room_key}
		rooms.append(obj)
	cont = {'chatbox':rooms}
	print(rooms)
	return render(request,'home.html',cont)

@authenticated
def get_logined_user(request):
	user = ""
	if request.user.is_authenticated:
		user = request.user.username
	else:
		user = "Anynomous"
	return JsonResponse({'user':user})

@unauthenticated
def register(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		new_user = User.objects.create_user(username = email)
		print(email, ' ',password)
		new_user.email = email
		new_user.set_password(password)
		new_user.save()
		messages.success(request, f"User created {new_user.username} ")
		login(request,new_user)
		messages.success(request,f'Logged in successfully')
		return redirect('social:home')
		

	return render(request, 'register.html')


@login_required(login_url="/login/")
def user_logout(request):
	logout(request)
	messages.success(request, 'Logged out')
	return redirect('social:home')

	
@unauthenticated
def user_login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=email, password=password)
		if user is not None:
			login(request, user)
			messages.success(request,'Logged in')
			return redirect('social:home')
		else:
			messages.error(request, 'Wrong Credentials')
			print(user)
		print(email, ' ',password)
	return render(request, 'login.html')

