from django.urls import path
from .views import *


app_name = "chatting"

urlpatterns = [
path("", test, name = "test"),
]