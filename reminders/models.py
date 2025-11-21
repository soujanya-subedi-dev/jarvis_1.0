from django.db import models
from django.conf import settings
from tasks.models import Task
from events.models import Event
from notes.models import Note

class Reminder(models.Model):
    REMINDER_TYPE_CHOICES = (
        ('task', 'Task'),
        ('event', 'Event'),
        ('note', 'Note'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=10, choices=REMINDER_TYPE_CHOICES)
    
    # Links to the related object (nullable for flexibility)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, null=True, blank=True, on_delete=models.CASCADE)

    message = models.TextField(blank=True)  # Optional custom message
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.reminder_type} Reminder"
