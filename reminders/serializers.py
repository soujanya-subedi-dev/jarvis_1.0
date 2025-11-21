from rest_framework import serializers
from .models import Reminder

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'reminder_type', 'task', 'event', 'note', 'message', 'remind_at', 'sent']
