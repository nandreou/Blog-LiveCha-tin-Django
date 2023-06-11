from django import forms
from .models import *

class RoomForm(forms.ModelForm):
    
    class Meta:
        model = Room
        fields = ['topic', 'name']

class MsgForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ['msg']

class AnsForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['answer']


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Useranme')
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)
