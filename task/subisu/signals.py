from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Activities, ActivityTable
from django.contrib.auth import get_user_model

@receiver(post_save, sender = Activities)
def create_comment(sender, instance, created, **kwargs):
    if created:
            title = instance.title
            startTime = instance.startTime
            ETA = instance.ETA
            endTime = instance.endTime
            activities = instance.activities
            createdTime = instance.created
            comment = instance.comment
            tableComment = f"Title : {title} \nStartTime : {startTime} \nETA : {ETA} \nEndTime : {endTime} \nActivities : {activities} \nCreatedAt : {createdTime} \nComment : {comment}"
            ActivityTable.objects.create(actId = instance, comment = tableComment)
        
