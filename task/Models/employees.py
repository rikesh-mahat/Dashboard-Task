from django.db import models

class Employees(models.Model):
    empName = models.CharField(max_length=200)
    mobile = models.BigIntegerField()
    email  = models.EmailField()
    cugNumber = models.BigIntegerField()
    branch = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    working = models.CharField(max_length=50)
    empGroup = models.CharField(max_length=200)
    supervisor1 = models.CharField(max_length=150)
    supervisor2 = models.CharField(max_length=150)
    
    def __str__(self):
        return self.empName