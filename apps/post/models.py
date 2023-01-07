from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}___{self.title}'

    class Meta:
        ordering = ('-create_at',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostImage(models.Model):
    image = models.ImageField(upload_to='post_images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')

    def __str__(self):
        return f'IMG:--{self.post.user}--{self.id}'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Картинка к посту'
        verbose_name_plural = 'Картинки к посту'



class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved')

    def __str__(self):
        return f"SAVE:    {self.user}--{self.post.title}"

    class Meta:
        ordering = ('id',)
        verbose_name = 'Сохранённое'
        verbose_name_plural = 'Сохранённые'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked')

    def __str__(self):
        return f"LIKE:    {self.user}--{self.post.title}"

    class Meta:
        ordering = ('id',)
        verbose_name = 'Лайкнутый'
        verbose_name_plural = 'Лайкнутые'
    
    