from django.db import models
from Models.units import Units

class Staffs(models.Model):
    firstName = models.CharField(max_length = 100)
    middleName = models.CharField(max_length=100, null = True, blank = True)
    lastName = models.CharField(max_length=100)
    empId = models.IntegerField()
    unitId = models.ForeignKey(Units, on_delete=models.PROTECT)
    email = models.EmailField()
    status = models.BooleanField(default= True)
    
    
    def __str__(self):
        if self.middleName:
            return self.firstName +" " +  self.middleName + " " + self.lastName 
        return self.firstName + " " + self.lastName 