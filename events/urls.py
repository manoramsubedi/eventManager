from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateEvent, name="create-event"),
]
