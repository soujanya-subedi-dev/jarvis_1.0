from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from reminders.models import Reminder

class Command(BaseCommand):
    help = "Send due reminders via email"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        reminders = Reminder.objects.filter(remind_at__lte=now, sent=False)

        for reminder in reminders:
            msg = reminder.message
            if not msg:
                if reminder.reminder_type == 'task' and reminder.task:
                    msg = f"Task '{reminder.task.title}' is due soon!"
                elif reminder.reminder_type == 'event' and reminder.event:
                    msg = f"Event '{reminder.event.title}' is starting soon!"
                elif reminder.reminder_type == 'note' and reminder.note:
                    msg = f"Reminder for note: '{reminder.note.title}'"

            send_mail(
                "Jarvis Reminder",
                msg,
                "noreply@jarvis.com",
                [reminder.user.email],
            )
            reminder.sent = True
            reminder.save()
            self.stdout.write(f"Sent reminder to {reminder.user.username}")
