import json

from django.shortcuts import render, redirect
from django.views import View
from .forms import EventForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


#JSON-File
JSON_FILE = "events.json"

def load_events():
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_events(events):
    with open(JSON_FILE, 'w') as file:
        json.dump(events, file) #serialize the events object to a json


class ViewEvent(View):
    def get(self, request):
        events = load_events()
        context = {'events':events}
        return render(request,"events/listevent.html",context)
    
class CreateEvent(LoginRequiredMixin, View):
    def get(self, request):
        form = EventForm #initializing empty form
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
        return render( request, "events/event_form.html", form)