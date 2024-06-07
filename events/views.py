import json
import os
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

# from datetime import date

#JSON-File
JSON_FILE = "events.json"

def load_events():
    if not os.path.exists(JSON_FILE) or os.path.getsize(JSON_FILE) == 0:
        # File does not exist or is empty
        return []

    try:
        with open(JSON_FILE, 'r') as file:
            events = json.load(file)
            return events
    except json.JSONDecodeError:
        # Handle the case where the file contains invalid JSON
        return []
    
def save_events(events):
    # Convert date objects to strings in ISO format
    for event in events:
        if isinstance(event['start_date'], date):
            event['start_date'] = event['start_date'].isoformat()
        if isinstance(event['end_date'], date):
            event['end_date'] = event['end_date'].isoformat()
    
    with open(JSON_FILE, 'w') as file:
        json.dump(events, file)


class ViewEvent(View):
    def get(self, request):
        events = load_events()
        context = {'events':events}
        return render(request,"events/listevent.html",context)
    
class CreateEvent(LoginRequiredMixin, View):
    def get(self, request):
        form = EventForm() #initializing empty form
        context = {'form': form}
        return render(request, "events/event_form.html", context)
    
    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            events = load_events() #load existing events
            events.append(form.cleaned_data) 
            save_events(events)
            return redirect("list-event")
        context = {'form':form}
        return render( request, "events/event_form.html", context)
    
class UpdateEvent(LoginRequiredMixin, View):
    def get(self, request, pk):
        events = load_events()
        event = events[int(pk)]
        form = EventForm(initial=event) #prefilled form with data related to the index
        context = {'form':form, 'pk':pk}
        return render(request, "events/event_form.html", context)
    
    def post(self, request, pk):
        form = EventForm(request.POST)
        if form.is_valid():
            events = load_events()
            events[int(pk)] = form.cleaned_data
            save_events(events)
            return redirect('list-event')
        context = {'form': form, 'pk':pk}
        return render(request, "events/event_form.html", context)
    
class DeleteEvent(LoginRequiredMixin,View):
    def get(self, request, pk):
        events = load_events()
        events.pop(int(pk))
        save_events(events)
        return redirect('list-event')

#Filters
@login_required
def filter_events(request):
    events = load_events()
    title = request.GET.get('title','').lower()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    filtered_events = []
    for event in events:
        if title and title not in event['title'].lower():
            continue
        if start_date and event['start_date'] < start_date:
            continue
        if end_date and event['end_date'] > end_date:
            continue
        filtered_events.append(event)

    return JsonResponse(filter_events, safe=False)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'events/login.html', context)

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'events/signup.html', context)

def user_home(request):
    return render(request, 'events/home.html')

def user_logout(request):
    logout(request)
    return redirect('login')
        
        

    