from django.db import models

from apps.post.models import Post

class Tag(models.Model):
    title = models.CharField(max_length=20)
    post = models.ManyToManyField(Post, related_name='tags')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-id',)
