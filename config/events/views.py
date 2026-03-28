from rest_framework import generics
from .models import Registration, Event
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.permissions import IsAdminUser
from .serializers import EventSerializer


class RegisterView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]


class CancelRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_id = request.data.get('event')

        try:
            registration = Registration.objects.get(
                user=request.user,
                event_id=event_id,
                status='registered'
            )
            registration.status = 'cancelled'
            registration.save()

            return Response({"message": "Registration cancelled"}, status=200)

        except Registration.DoesNotExist:
            return Response({"error": "Registration not found"}, status=404)
        

class EventStatsView(APIView):
    def get(self, request):
        data = []

        events = Event.objects.all()

        for event in events:
            registered_count = Registration.objects.filter(
                event=event, status='registered'
            ).count()

            available_slots = event.capacity - registered_count

            data.append({
                "event": event.title,
                "registered_users": registered_count,
                "available_slots": available_slots
            })

        return Response(data)
    

class TopEventsView(APIView):
    def get(self, request):
        events = Event.objects.annotate(
            registrations_count=Count('registration')
        ).order_by('-registrations_count')[:5]

        data = [
            {
                "event": event.title,
                "registrations": event.registrations_count
            }
            for event in events
        ]

        return Response(data)
    
class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer