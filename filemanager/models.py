from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class File(models.Model):
    CATEGORY_CHOICES = (
        ('document', 'Document'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('code', 'Code'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"
