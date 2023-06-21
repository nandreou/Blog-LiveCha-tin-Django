from django.urls import path
from .views import *


app_name = "chatting"

urlpatterns = [
path("", Chat_Rooms, name = "chatrooms"),
path("ChatRoom/<str:roomkey>/", Chat_Room, name = "room"),
path("CreateRoom/", CreateChatRoom, name = "CreateRoom"),
path("DeleteRoom/<str:roomkey>/", DeleteChatRoom, name = "DeleteRoom")
]