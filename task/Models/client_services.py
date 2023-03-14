from django.db import models
from Models.hosts import Hosts
from Models.serviceTypes import ServiceTypes
from django.core.exceptions import ValidationError


def mobile_number_validation(value):
    if len(value) != 10:
        raise ValidationError("Invalid Mobile Number")
    else:
        try:
            int(value)
        except:
            raise ValidationError("Alphabets or Symbols not allowed")

class ClientServices(models.Model):
    domainName = models.CharField(max_length=250)
    srvType = models.ForeignKey(ServiceTypes, on_delete=models.PROTECT)
    hostId = models.ForeignKey(Hosts, on_delete=models.PROTECT)
    email = models.EmailField()
    primaryContactName = models.CharField(max_length=250)
    primaryContactNumber = models.BigIntegerField(validators=[mobile_number_validation])
    primaryContactEmail = models.EmailField()
    secondaryContactName =models.CharField(max_length=250)
    secondaryContactNumber = models.BigIntegerField(validators=[mobile_number_validation])
    secondaryContactEmail = models.EmailField()
    serviceStatus = models.BooleanField(default = True)
    serviceCreatedData = models.DateTimeField()
    
    def __str__(self):
        return self.primaryContactName