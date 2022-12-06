from inst_api.celery import app
from celery import shared_task
from time import sleep


from apps.story.models import Story

@shared_task
def archive_story(id_story):
    try:
        story = Story.objects.get(id=id_story)
        sleep(86400)
        story.is_archived = True
        story.save()
    except Exception as _ex:
        print(_ex)

    

