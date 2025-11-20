from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer

class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).order_by('date', 'time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


# Upcoming Events
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

class UpcomingEventsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        next_week = today + timedelta(days=7)

        events = Event.objects.filter(
            user=request.user,
            date__gte=today,
            date__lte=next_week
        ).order_by('date', 'time')

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
