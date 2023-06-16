import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from subisu.models import Activities, EmailNotification
from subisu.emails import send_department_mail
from django.contrib import messages



@receiver(post_save, sender=Activities)
def create_email(sender, instance, created, **kwargs):
    if created and instance.sendEmail:
        EmailNotification.objects.create(activityId = instance, emailBody = "\n".join([instance.title, instance.location, instance.reason, instance.impact]))
        
       



