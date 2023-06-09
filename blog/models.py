from multiprocessing.connection import answer_challenge
from typing import ChainMap
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.deletion.CASCADE)
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    name = models.CharField(max_length=100, primary_key=True)
    updated = models.DateField(auto_now_add=True)
    created = models.DateField(auto_now=True)
    participants = models.ManyToManyField(User, related_name= 'participants', blank = False)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.deletion.CASCADE)
    msg = models.TextField()
    updated = models.DateField(auto_now_add=True)


class Answers(models.Model):
    msg = models.ForeignKey(Message, on_delete=models.deletion.CASCADE)
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    answer = models.TextField()
    
    
