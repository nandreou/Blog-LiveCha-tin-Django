from http.client import INTERNAL_SERVER_ERROR
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

class AnswerToMessage(LoginRequiredMixin, View):
    login_url = "blog:UserLogin"
    def get(self, request,roomkey = None, namekey = None):
        return render(request, "msg.html", {'form': MsgForm()})
    
    def post(self, request,roomkey = None ,namekey = None):
        form = MsgForm(request.POST)

        if form.is_valid():
            Answers.objects.create(msg = Message.objects.get(id = namekey), answer = form.cleaned_data['msg'], user = User.objects.get(username = request.user.username))
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    print(f"{field}: {error}")
        return redirect("blog:room-env", roomkey)

class EditAnswer(View):
    login_url = "blog:UserLogin"
    def get(self, request, roomkey = None, anskey = None):
            return render (request, "msg.html", {'form': AnsForm(initial ={'answer': Answers.objects.get(id = anskey).answer})})
    
    def post(self,request, roomkey = None,anskey = None):
        form = AnsForm(request.POST, instance = get_object_or_404(Answers, id = anskey))

        if form.is_valid():
            form.save()
        else:
            print("something went wrong")
        
        return redirect("blog:room-env", roomkey)


class DeleteAnswer(View):
    login_url = "blog:UserLogin"
    def get(self, request, roomkey= None ,anskey = None):
        return render (request, "delete.html", {'rooms': Room.objects.get(name = roomkey)})

    def post(self, request, roomkey = None,anskey = None):
        Answers.objects.get( id = anskey).delete()
        return redirect('blog:room-env', roomkey)
    