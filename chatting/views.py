from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import redirect, get_object_or_404

# Create your views here.

@login_required(login_url="blog:UserLogin")
def Chat_Rooms(request, *args, **kwargs):
    return render(request, 'chatting/chat_rooms.html', {'rooms': ChatRoom.objects.all()})

@login_required(login_url="blog:UserLogin")
def CreateChatRoom(request):
    if request.method == 'GET':
        return render(request, "chatting/createchat.html", {'form': ChatRoomForm()})
    
    elif request.method == 'POST':   
        form = ChatRoomForm(request.POST or None)
        if form.is_valid():
            print('success', form.cleaned_data)
            ChatRoom.objects.create(**form.cleaned_data, chat_user = User.objects.get(username = request.user.username))
            return redirect("chatting:chatrooms")
        else:
            print("Nope")
            return render(request, "chatting/createchat.html", {'form': ChatRoomForm()})

def DeleteChatRoom(request, roomkey):
    if request.method == 'GET':
        return render (request, "chatting/chatdelete.html", {'room': ChatRoom.objects.get(chat_name = roomkey)})
    elif request.method == 'POST':
        ChatRoom.objects.get(chat_name = roomkey).delete()
        return redirect("chatting:chatrooms")

@login_required(login_url="blog:UserLogin")
def Chat_Room(request, roomkey,*args, **kwargs):
    return render(request, 'chatting/chat.html', {'roomkey': roomkey})