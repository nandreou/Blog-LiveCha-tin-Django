from django.shortcuts import render
from django.views.generic import View
from .models import *
from .forms import *
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import django.http
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

class HomePage(View):
    
    def get(self, request, *args, **kargs):
        return render(request, "home.html", {'rooms': Room.objects.all()})


class CreateRoom(LoginRequiredMixin ,View):
    login_url = 'blog:UserLogin'
    def get(self,request, *args, **kargs):
        return render(request, "create.html", {'form': RoomForm()})

    def post(self,request, *args, **kwargs):
        form = RoomForm(request.POST or None)
        if form.is_valid():
            Room.objects.create(**form.cleaned_data, user = User.objects.get(username = request.user.username))
    
        return redirect("blog:home")
    
class RoomField(View):
    
    def get(self, request, namekey=None, *args, **kwargs):
        return render(request, "room.html", {'rooms': Room.objects.get(name = namekey), 'messages': Message.objects.filter(room = Room.objects.get(name = namekey)), 'participants' : Room.objects.get(name = namekey).participants.all()})

class MessageCreate(LoginRequiredMixin, View):
    login_url = 'blog:UserLogin'
    def get(self, request, *args, **kwargs):
        return render(request, "msg.html", {'form': MsgForm()}) 

    def post(self, request,namekey= None, *args, **kwargs):
        
        form = MsgForm(request.POST)
        if form.is_valid():
            Message.objects.create(**form.cleaned_data, room=Room.objects.get(name = namekey), user = User.objects.get(username = request.user.username))
            Room.objects.get(name = namekey).participants.add(User.objects.get(username = request.user.username))    
        return redirect("blog:room-env", namekey)

class MessageUpdate(View):
    
    def get(self, request, msgid = None, *args, **kwargs):
        return render(request, "msg.html", {'form': MsgForm(initial={'msg': Message.objects.get(id=msgid).msg})})
    
    def post(self, request, namekey= None, msgid = None, *args, **kwrgs):
        
        form = MsgForm(request.POST, instance = get_object_or_404(Message, id = msgid))
        if form.is_valid():
            form.save()
        return redirect("blog:room-env", namekey)

class DeleteRoom(LoginRequiredMixin, View): #The restrictions of log in are done with LoginRequiredMixin in vies. In functional is @login_required
    login_url = 'blog:UserLogin'
    
    def get(self, request, pk=None, *args, **kargs):
        if request.user.username == 'nick':
            return render(request, "delete.html", {'rooms': Room.objects.get(name = pk)})
        else:
            return django.http.HttpResponse("<h1>Need to be admin to perform this action</h1> <br> <a href= http://127.0.0.1:8000/home> Home </a> ") #this is Temporary

    def post(self, request, pk=None,*args, **kargs):
        Room.objects.get(name = pk).delete()
        return redirect('blog:home') 


#USER SETTINGS FIELD
class UserLogin(View):
     
    def get(self, request, *args, **kwargs):
        return render(request, "login.html", {'form': UserLoginForm()})

    def post(self, request, *args, **kwrags):
        
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
                user = authenticate(request, **form.cleaned_data)
                if user is not None:
                    login(request, user)
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    print(f"{field}: {error}")
        return redirect("blog:home")

class RegisterUser(View):
 
    def get(self, request, *args, **kwargs):
        return render(request, "signup.html", {'form': UserCreationForm()})
    
    def post(self, request):

        form = UserCreationForm(request.POST or None)

        if form.is_valid():
            form.save()
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    print(f"{field}: {error}") 
        
        return redirect("blog:home")
    
class ChangePassword(LoginRequiredMixin, View): #note there is no need for so much html files
    login_url = 'blog:UserLogin'

    def get(self, request):
        if request.user != None:
            return render(request, "pass.html", {'form':PasswordChangeForm(request.user)})
    
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            update_session_auth_hash(request, form.save())
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    print(f"{field}: {error}")

        logout(request)
        return redirect("blog:home")


class DeleteMessage(View):
     
    def get(self, request, namekey = None, msgid = None):
        print(namekey, msgid)
        return render(request, "delete-msg.html", {'room': Room.objects.get(name = namekey), 'msg': Message.objects.get(id = msgid)})

    def post(self, request, namekey=None, msgid = None):
        Message.objects.get(id = msgid).delete()
        return redirect('blog:room-env', namekey)
    
    

@login_required(login_url="blog:UserLogin")
def Userlogout(request, *args, **kwargs):
    logout(request)
    return redirect("blog:home")


#TODO Use flash messages to display errors
#TODO add answers to the project