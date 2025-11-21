from rest_framework import serializers
from tasks.serializers import TaskSerializer
from notes.serializers import NoteSerializer
from events.serializers import EventSerializer
from reminders.serializers import ReminderSerializer
from filemanager.serializers import FileSerializer

class DashboardSerializer(serializers.Serializer):
    tasks = TaskSerializer(many=True)
    notes = NoteSerializer(many=True)
    events = EventSerializer(many=True)
    reminders = ReminderSerializer(many=True)
    files = FileSerializer(many=True)
