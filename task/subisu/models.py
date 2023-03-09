from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .emails import send_department_email
# this is my mobile validation function
def mobile_no_length(number):
    try:
        number  = int(number)
    except:
        raise ValidationError("Sorry the number cannot contaain any symbols or alphabets")
    if len(str(number)) != 10:
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


class Host(models.Model):

    dcID = models.ForeignKey(Datacenter, on_delete=models.CASCADE, verbose_name="Select Datacenter")
    hostname = models.CharField(max_length=200, verbose_name="Host Name")
    ip = models.CharField(max_length=250, verbose_name="Internet Protocol Address (IP Addres)", validators=[ip_address])  # ip validator haleko chu esma
    remarks = models.TextField(null=True, blank=True, verbose_name="Remarks", help_text="Leave remakrs for the host")
    
    def __str__(self):
        return self.hostname

class ServiceType(models.Model):

    serviceName = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.serviceName
     
class Service(models.Model):

    hostId = models.ForeignKey(Host,on_delete=models.CASCADE, verbose_name="Select Host", null=True, related_name='services')
    srvType = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Select Service Type")
    hostName = models.CharField(max_length=200, null=True, blank=True, verbose_name="Host Name", help_text="Enter Host Name", editable=False)
    remarks = models.TextField(null=True, blank=True, verbose_name="Remark", help_text="Leave a remark")
    created = models.TimeField(auto_now_add=True, verbose_name="Created At")
    
    
    def save(self, *args, **kwargs):
        hostObj = Host.objects.get(id = self.hostId.id)
        self.hostName = hostObj.hostname
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
    
# department section

class Department(models.Model):

    name = models.CharField(max_length=100, verbose_name="Department Name")
    email = models.EmailField(max_length=200, verbose_name="Department Email")
    status = models.BooleanField(default = True, verbose_name="Department Status")
    
    
    def __str__(self):
        return self.name
    
    
class Staff(models.Model):

    firstName = models.CharField(max_length=50, verbose_name="First Name")
    middleName = models.CharField(max_length=50, verbose_name="Middle Name", null=True, blank=True)
    lastName = models.CharField(max_length=50, verbose_name="Last Name")
    deptId = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Select Department")
    email = models.EmailField(max_length= 200, verbose_name="Staff Email")
    mobile = models.CharField(max_length=15, verbose_name="Staff Mobile No", validators=[mobile_no_length])
    registerDate = models.TimeField(auto_now_add=True, verbose_name="Registered At")
    
    def __str__(self):
        if self.middleName == None:
            return  self.firstName + " " +self.lastName
        return self.firstName + " "+ self.middleName +  " " +self.lastName


ACTIVITY_STATUS = [
    ('Pending', 'Pending'),
    ('Open' , 'Open'),
    ('Close', 'Close'),
    ('In Progress', 'In Progress')
]    
    
class Activities(models.Model):
    title = models.CharField(max_length=200, verbose_name="Activity Title")
    startTime = models.DateTimeField(auto_now=False, verbose_name="Activity Start Time")
    ETA = models.CharField(max_length=200)
    endTime = models.DateTimeField(auto_now=False, verbose_name="Activity End Time")
    activities = models.TextField(max_length=500, verbose_name="Activities")
    created = models.TimeField(auto_now_add=True, verbose_name="Activity Created At")
    comment = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ACTIVITY_STATUS, default='Open')
    sendEmail = models.BooleanField(verbose_name="Send Email", help_text="Send Email to Department", default=False)

    def save(self, *args, **kwargs):
        if self.id:
            # create gareko cha ki nai check huncha ani save garda feri arko table banaidincha activities table ma save garesi 
            title = self.title
            startTime = self.startTime
            ETA = self.ETA
            endTime = self.endTime
            activities = self.activities
            createdTime = self.created
            comment = self.comment
            tableComment = f"Title : {title} \nStartTime : {startTime} \nETA : {ETA} \nEndTime : {endTime} \nActivities : {activities} \nCreatedAt : {createdTime} \nComment : {comment}"
            ActivityTable.objects.create(actId = self, comment = tableComment, commentBy = User.objects.filter(is_superuser = True).first().username) # for superusername yours might be commentedBy
        # if self.sendEmail:
        #     dep_email = Department.objects.all().first().email
        #     if dep_email:
        #         send_department_email(self.title, self.activities, dep_email)
        super(Activities, self).save(*args, **kwargs)  
        
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
    fieldEngineer = models.ManyToManyField(Staff, blank=True, verbose_name="Select Field Engineers")
    poaDetails = models.TextField(max_length=250, verbose_name="POA Details")
    poaEntry = models.TimeField(auto_now_add=True, verbose_name="POA Entry")
    
    
    def __str__(self):
        activityObj = Activities.objects.get(id = self.activityId.id)
        return "POA : " + str(activityObj.title)
    
    
    
    
    

class EmailNotification(models.Model):

    activityId = models.ForeignKey(Activities, on_delete=models.CASCADE, verbose_name="Select Activity")
    # email = models.EmailField(max_length=200, verbose_name="Email")
    # sendStatus = models.CharField(max_length=25, verbose_name="Status")
    emailBody = models.TextField(null=True, blank=True)
    logTime = models.TimeField(auto_now_add=True)
    
    # def save(self, *args, **kwargs):
    #     if self.sendStatus == 'In Progress':
    #         self.sendTo = 'Department'
    #         self.message = self.activityId.activities
    #     super(EmailNotification, self).save(*args, **kwargs)  
        
    # def __str__(self):
    #     return self.email