from django.shortcuts import render
from django.views.generic import View
from .models import *
from .forms import *
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfile(View):
    def get(self, request, user_name = None):
        return render(request, "userprof.html", {'participate': [[room.name, room.topic.name, room.user] for room in Room.objects.all() for _ in room.participants.filter(username__icontains = user_name)], 'rooms': Room.objects.filter(user__username__icontains = user_name)})
    