from django.urls import path
from . import views

app_name = "blog"

urlpatterns= [
    path('home/', views.HomePage.as_view(), name = "home"),
    path('delete/<str:pk>', views.DeleteRoom.as_view(), name = "delete"),
    path('room/<str:namekey>', views.RoomField.as_view(), name = "room-env"),
    path('create/', views.CreateRoom.as_view(), name = "create"),
    path('message/<str:namekey>', views.MessageCreate.as_view(), name = 'message-create'),
    path('UserLogin/', views.UserLogin.as_view(), name = 'UserLogin'),
    path('UserLogout', views.Userlogout, name = "UserLogout"),
    path('RegisterUser/', views.RegisterUser.as_view(), name = "SignUp"),
    path('ChangePassword/', views.ChangePassword.as_view(), name = "ChangePassword"),
    path('DeleteMessage/<str:namekey>/<str:msgid>', views.DeleteMessage.as_view(), name = "DeleteMessage"),
    path("room/<str:namekey>/EditMessage/<int:msgid>", views.MessageUpdate.as_view(), name = "EditMessage")
]