from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_department_mail(title, maintenance, location, reason, benefits, impact , contact):
    sender = settings.EMAIL_HOST_USER
    subject  = title
    receiver = contact
    
    
    
    context = {'title' : title, 'maintenance' : maintenance, 'location' : location, 'reason' : reason, 'benefits' : benefits, 'impact' : impact}
    html_content = render_to_string('subisu/departmentmail.html', context)
    text_content = strip_tags(html_content)
    
    msg = True
    try:
        email_message = EmailMultiAlternatives(subject, text_content, sender, receiver)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
    except:
        msg = False
    return msg

def send_poa_emails(subject, message, receiver):
    sender = settings.EMAIL_HOST_USER 
    if receiver:
        send_mail(subject, message, sender, receiver)