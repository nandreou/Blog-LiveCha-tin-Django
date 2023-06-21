from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatTopic(models.Model):
    topic = models.TextField(max_length=100, primary_key=True)

class ChatRoom(models.Model):
    chat_topic = models.ForeignKey(ChatTopic, on_delete=models.deletion.CASCADE)
    chat_user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    chat_name = models.TextField(max_length=100, primary_key=True)
    updated = models.DateField(auto_now_add=True)
    created = models.DateField(auto_now=True)

