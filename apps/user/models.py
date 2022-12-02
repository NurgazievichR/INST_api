from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)
    bio = models.CharField(max_length=255, blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username 

    class Meta: 
        ordering = ('-id',)

