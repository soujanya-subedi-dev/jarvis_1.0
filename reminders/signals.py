# reminders/signals.py
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from events.models import Event
from .models import Reminder

@receiver(post_save, sender=Task)
def create_task_reminder(sender, instance, created, **kwargs):
    if created and instance.deadline:
        Reminder.objects.create(
            user=instance.user,
            task=instance,
            reminder_type='task',
            remind_at=instance.deadline - timedelta(hours=1),  # 1 hour before
            message=f"Task '{instance.title}' is due soon!"
        )

@receiver(post_save, sender=Event)
def create_event_reminder(sender, instance, created, **kwargs):
    if created and instance.start_time:
        Reminder.objects.create(
            user=instance.user,
            event=instance,
            reminder_type='event',
            remind_at=instance.start_time - timedelta(minutes=30),  # 30 min before
            message=f"Event '{instance.title}' is starting soon!"
        )
