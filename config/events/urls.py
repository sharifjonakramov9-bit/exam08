from django.urls import path
from .views import RegisterView, CancelRegistrationView, EventListView, EventStatsView, TopEventsView, EventCreateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('cancel/', CancelRegistrationView.as_view()),
    path('stats/', EventStatsView.as_view()),
    path('top-events/', TopEventsView.as_view()),
    path('create-event/', EventCreateView.as_view()),
    path('events/', EventListView.as_view()),
]