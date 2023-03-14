from django.db import models
from Models.departments import Departments
class Units(models.Model):
    name = models.CharField(max_length = 100)
    departmentId = models.ForeignKey(Departments, on_delete=models.PROTECT)
    unitHead = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name