from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from events.models import Event
from .serializers import CalendarTaskSerializer, CalendarEventSerializer

from reminders.models import Reminder
from reminders.serializers import ReminderSerializer

class TodayCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = datetime.now()

        tasks = Task.objects.filter(user=user, deadline__date=now.date())
        events = Event.objects.filter(user=user, start_time__date=now.date())
        reminders = Reminder.objects.filter(user=user, remind_at__date=now.date(), sent=False)

        return Response({
            "tasks": CalendarTaskSerializer(tasks, many=True).data,
            "events": CalendarEventSerializer(events, many=True).data,
            "reminders": ReminderSerializer(reminders, many=True).data
        })

class WeekCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = datetime.now().date()
        week_later = today + timedelta(days=7)

        tasks = Task.objects.filter(user=user, deadline__date__range=[today, week_later])
        events = Event.objects.filter(user=user, start_time__date__range=[today, week_later])

        return Response({
            "tasks": CalendarTaskSerializer(tasks, many=True).data,
            "events": CalendarEventSerializer(events, many=True).data
        })

class MonthCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = datetime.now().date()
        first_day = today.replace(day=1)
        if today.month == 12:
            last_day = today.replace(year=today.year+1, month=1, day=1)
        else:
            last_day = today.replace(month=today.month+1, day=1)

        tasks = Task.objects.filter(user=user, deadline__date__range=[first_day, last_day])
        events = Event.objects.filter(user=user, start_time__date__range=[first_day, last_day])

        return Response({
            "tasks": CalendarTaskSerializer(tasks, many=True).data,
            "events": CalendarEventSerializer(events, many=True).data
        })

class AgendaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        tasks = Task.objects.filter(user=user).order_by('deadline')
        events = Event.objects.filter(user=user).order_by('start_time')

        return Response({
            "tasks": CalendarTaskSerializer(tasks, many=True).data,
            "events": CalendarEventSerializer(events, many=True).data
        })
