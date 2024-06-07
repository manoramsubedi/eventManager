from django.urls import path
from .views import *

urlpatterns = [
    path('',user_home, name='home'),

    path('login', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    
    path('listevent/', ViewEvent.as_view(), name='list-event'),  # List events
    path('event_form/', CreateEvent.as_view(), name='create-event'),  # Create new event
    path('edit/<int:pk>/', UpdateEvent.as_view(), name='update-event'),  # Edit event
    path('delete/<int:pk>/', DeleteEvent.as_view(), name='delete-event'),  # Delete event
    path('filter/', filter_events, name='event-filter'),  # Filter event
]