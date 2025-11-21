from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')   # preferences
    prefer_email_notifications = models.BooleanField(default=True)
    # add more preferences fields as needed

    def __str__(self):
        return self.user.username

# Create/Update profile automatically
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
