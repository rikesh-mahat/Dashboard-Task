from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from Models.units import Units
from Models.serviceTypes import ServiceTypes
from Models.departments import Departments
from Models.hosts import Hosts
from Models.staffs import Staffs
from django.utils import timezone
from django.core.validators import validate_email
from datetime import timedelta


def validate_email_list(value):
    # validation multiple email list
    emails = value.split()
    for email in emails:
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Invalid email address: {}'.format(email))
def mobile_no_length(number):
    try:
        number  = int(number)
    except:
        raise ValidationError("Sorry the number cannot contaain any symbols or alphabets")
    num = str(number)
    if len(num) != 10:
        raise ValidationError("Mobile Number digits should be exactly 10")

# yoh chai ip validation function 
def ip_address(ip):
    ip_list = ip.split('.')
    length = len(ip_list)
    if length == 4:
        for ip_value in ip_list:
            try:
                if (int(ip_value) > 255):
                    raise ValidationError("Invalid IP Address")
            except:
                raise ValidationError("Invalid Character in IP Address")
    else:
        raise ValidationError('Invalid IP Address')
    
class Datacenter(models.Model):
   
    name = models.CharField(max_length= 200, verbose_name="Datacenter Name")
    address = models.CharField(max_length=200, verbose_name="Datacenter Address")
    contact = models.BigIntegerField(verbose_name="Datacenter Contact")
    remarks = models.TextField(null=True, blank=True, help_text="Leave remarks for the datacenter")
    
    def __str__(self):
        return self.name



     
class Service(models.Model):

    hostId = models.ForeignKey(Hosts,on_delete=models.CASCADE, verbose_name="Select Host", null=True, related_name='services')
    srvType = models.ForeignKey(ServiceTypes, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Select Service Type")
    hostName = models.CharField(max_length=200, null=True, blank=True, verbose_name="Host Name", help_text="Enter Host Name", editable=False)
    remarks = models.TextField(null=True, blank=True, verbose_name="Remark", help_text="Leave a remark")
    created = models.TimeField(auto_now_add=True, verbose_name="Created At")
    
    
    def save(self, *args, **kwargs):
        self.hostName = self.hostId.hostname
        super(Service, self).save(*args, **kwargs)  
        
    def __str__(self):
        return self.srvType.serviceName
    
    
class ClientContact(models.Model):
    srvid = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name="Select Service")
    name=  models.CharField(max_length=200, verbose_name="Full Name")
    mobile = models.CharField(max_length=200, verbose_name="Mobile Number", validators=[mobile_no_length]) # esma mobile
    email = models.EmailField(max_length=150, verbose_name="Email")
    status = models.BooleanField(default=True, verbose_name="Client Status")
    registerDate = models.TimeField(auto_now_add=True, verbose_name="Register Date")
    
    
    def __str__(self):
        return self.name
    

    


ACTIVITY_STATUS = [
    ('Pending', 'Pending'),
    ('Open' , 'Open'),
    ('Close', 'Close'),
]    
    
class Activities(models.Model):
    title = models.CharField(max_length=200, verbose_name="Activity Title")
    
    location = models.CharField(max_length=200, null=True, blank=True)
    reason = models.TextField(verbose_name="Reasons", blank=True)
    benefits = models.TextField(verbose_name="Benefits for Layer", blank=True)
    impact = models.TextField(verbose_name="Impact", blank=True)
    contact = models.ForeignKey(Units, on_delete=models.CASCADE,  null=True, help_text="Select units you want to send mail to")
    startTime = models.DateTimeField(null=True, blank=True, verbose_name="Activity Start Time")
    endTime = models.DateTimeField(null=True, blank=True,verbose_name="Activity End Time")
    activities = models.TextField(max_length=500, verbose_name="Activities")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Activity Created At")
    otherEmails = models.TextField(blank=True, null=True, help_text="Add other emails separated by spaces", validators=[validate_email_list])
    Comment= models.CharField(max_length=200, null=True)
    status= models.CharField(max_length=20,choices=ACTIVITY_STATUS, default= 'Open')
    sendEmail = models.BooleanField(verbose_name = "Send Email",default=False, help_text="Send Email Notification to Department")
    ETA = models.CharField(max_length=200, null=True, blank=True, editable=False)

    def save(self):
        if self.startTime and self.endTime:
            duration = self.endTime - self.startTime

            if duration < timedelta(hours=1):
                self.ETA = f"{duration.seconds//60} min"
            elif duration < timedelta(hours=24):
                self.ETA = f"{duration.seconds//3600} hr"
            else:
                days = duration.days if duration.days > 1 else 1
                self.ETA = f"{days} day"
        super().save()
            
     
    
    def __str__(self):
        return self.title
    

class ActivityTable(models.Model):
    actId  = models.ForeignKey(Activities, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(max_length=500, null=True, blank=True, editable=False)
    commentBy = models.CharField(max_length=200, null=True,blank=True,editable=False)
    timeStamp = models.TimeField(auto_now_add=True, null=True)
    
  
        
    def __str__(self):
        return self.actId.title
    

class Poa(models.Model):
    activityId = models.ForeignKey(Activities, on_delete=models.CASCADE, verbose_name="Select Activity")
    fieldEngineer = models.ManyToManyField(Staffs, blank=True, verbose_name="Select Field Engineers")
    poaDetails = models.TextField(max_length=250, verbose_name="POA Details")
    poaEntry = models.TimeField(auto_now_add=True, verbose_name="POA Entry")
    sendEmail = models.BooleanField(default=True)
    units = models.ManyToManyField(Units, blank=True, verbose_name="Send emails to Units")
    
    def __str__(self):
        activityObj = Activities.objects.get(id = self.activityId.id)
        return "POA : " + str(activityObj.title)


class EmailNotification(models.Model):
    activityId = models.ForeignKey(Activities, on_delete=models.CASCADE, verbose_name="Select Activity")
    emailBody = models.TextField(null=True, blank=True)
    logTime = models.TimeField(auto_now_add=True)
