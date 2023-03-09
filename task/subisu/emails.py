from django.core.mail import send_mail
from django.conf import settings

def send_department_email(subject, message,receiver):
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender,[receiver])