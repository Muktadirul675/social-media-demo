from django.urls import path, include
from . import views

app_name = 'social'

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('<int:user2_id>/<str:key>/',views.room,name='room'),
    path('get_logined_user/',views.get_logined_user,name='get_logined_user')
]