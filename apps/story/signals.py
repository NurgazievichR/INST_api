from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.story.models import Story
from utils.celery_tasks import archive_story

@receiver(post_save, sender=Story)
def story_archive(**kwargs):
    instance = kwargs['instance']
    print('signal getted')
    archive_story.delay(id_story=instance.id)

