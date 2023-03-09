from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Activities, ActivityTable, EmailNotification, Poa, Department
from .emails import send_department_email
from django.contrib.auth.models import User

# signal : kunai acitivity create bhayesi signal aaucha ani hamley activitytable ma tyo comment haru automatically halchum


@receiver(post_save, sender=Activities)
# sender  = Activties, instance = Activities, created bhaneko create bhayo ki nai bhanera check garna lai
def email_and_comment(sender, instance, created, **kwargs):
    if created:
        title = instance.title
        startTime = instance.startTime
        ETA = instance.ETA
        endTime = instance.endTime
        activities = instance.activities
        createdTime = instance.created
        comment = instance.comment
        tableComment = f"Title : {title} \nStartTime : {startTime} \nETA : {ETA} \nEndTime : {endTime} \nActivities : {activities} \nCreatedAt : {createdTime} \nComment : {comment}"
        ActivityTable.objects.create(actId=instance, comment=tableComment, commentBy=User.objects.filter(
            is_superuser=True).first().username)  # your might be commentedBy

        if instance.sendEmail:
            body = f"Activities Remarks : {activities}"
            if instance.status == "Pending":
                poa_details = Poa.objects.filter(
                    activityId=instance).last().poaDetails
                body = activities
                if poa_details:
                    body += f"Poa Detail : {poa_details}"
            EmailNotification.objects.create(
                activityId=instance, emailBody=body)
            # actually sending the mail to user
            dep_email = Department.objects.all().first().email
            if dep_email:
                send_department_email(title, body, dep_email)
