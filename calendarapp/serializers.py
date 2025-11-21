from rest_framework import serializers
from tasks.models import Task
from events.models import Event

class CalendarTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'is_completed', 'priority']


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'location']
