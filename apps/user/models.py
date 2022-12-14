from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)
    bio = models.CharField(max_length=255, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False, null=True)
    hide_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username 

    class Meta: 
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_online(self):
        if timezone.now() - self.last_activity < timezone.timedelta(minutes=3):
            return True
        return False


class UserFollow(models.Model):
    to_user = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name="subscriptions", on_delete=models.CASCADE)
    is_confirmed = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return f"Subscribe {self.create_at} from {self.from_user} to {self.to_user}"

    class Meta:
        ordering = ('-create_at',)  
        unique_together = (('from_user', 'to_user'),)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    