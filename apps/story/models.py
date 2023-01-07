from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'stories' )
    create_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='stories', validators=[FileExtensionValidator(allowed_extensions=['mp4','mov','jpg','webp','jpeg','png'])])
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} STORY: {self.pk}'

    class Meta:
        ordering = ('-create_at',)
        verbose_name = 'Сторис'
        verbose_name_plural = 'Сторисы'

    

    