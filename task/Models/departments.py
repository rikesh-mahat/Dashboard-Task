from django.db import models

class Departments(models.Model):
    name = models.CharField(max_length = 100, unique=True, primary_key=True)
    email = models.EmailField()
    status = models.BooleanField(default = True)
    vpName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name