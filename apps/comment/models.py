from django.db import models
from django.contrib.auth import get_user_model

from apps.post.models import Post


User = get_user_model()



# class CommentManager(models.Manager):
#     def all(self):
#         return super(CommentManager, self).filter(parent=None)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self) -> str:
        return f'{self.user} to {self.post}, comment: {self.body}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-id',)
