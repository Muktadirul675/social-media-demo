from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
def authenticated(view_func):
	def wrapper_function(request, *args, **kwargs):
		if request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		else:
			messages.success(request, 'You need to login first!')
			return redirect('social:login')
	return wrapper_function

def unauthenticated(view_func):
	def wrapper_function(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('social:home')
		
	return wrapper_function


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_function(request, *args,**kwargs):
			verified = False
			for i in list(request.user.groups.all()):
				if i.name in allowed_roles:
					verified = True
				break
			if verified:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse("You are not allowed")
		return wrapper_function
	return decorator