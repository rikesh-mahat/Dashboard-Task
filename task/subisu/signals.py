from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Activities, Poa
from .emails import send_department_mail, send_poa_emails
from django.contrib.auth.models import User


@receiver(post_save, sender=Activities)

def activity_created(sender, instance, created, **kwargs):
    if created and instance.sendEmail:
        title = instance.title 
        maintenance = instance.maintenanceWindow
        location = instance.location
        reason = instance.reason
        benefits = instance.benefits
        impact = instance.impact
        unit_email = instance.contact.email
        department_email = instance.contact.departmentId.Email
        print(department_email, unit_email)
        contact_list = [unit_email, department_email]
        
        send_department_mail(title, maintenance, location, reason, benefits, impact, contact_list)
                




@receiver(m2m_changed, sender=Poa.units.through)
def poa_units_changed(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear'):
     
        poa = instance
        units = poa.units.all()
        unit_email_list = [unit.email for unit in units] if units.exists() else []
        
        if unit_email_list:
            subject = poa.activityId.title
            message = poa.poaDetails
            send_poa_emails(subject, message, unit_email_list)