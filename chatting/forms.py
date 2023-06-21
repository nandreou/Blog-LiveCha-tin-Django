from django import forms
from .models import *


class ChatRoomForm(forms.ModelForm):
    
    class Meta:
        model = ChatRoom
        fields = ['chat_topic', 'chat_name']
