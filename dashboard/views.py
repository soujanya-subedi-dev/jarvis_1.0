from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime, timedelta

from tasks.models import Task
from notes.models import Note
from events.models import Event
from reminders.models import Reminder
from filemanager.models import File

from .serializers import DashboardSerializer

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = datetime.now()

        # Fetch data from all modules
        tasks = Task.objects.filter(user=user).order_by('-created_at')[:10]  # latest 10
        notes = Note.objects.filter(user=user).order_by('-created_at')[:10]
        events = Event.objects.filter(user=user, start_time__gte=now).order_by('start_time')[:10]
        reminders = Reminder.objects.filter(user=user, sent=False, remind_at__gte=now).order_by('remind_at')[:10]
        files = File.objects.filter(user=user).order_by('-uploaded_at')[:10]

        data = {
            "tasks": tasks,
            "notes": notes,
            "events": events,
            "reminders": reminders,
            "files": files
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
