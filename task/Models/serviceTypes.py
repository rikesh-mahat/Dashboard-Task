from django.db import models

class ServiceTypes(models.Model):
    srvType = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    
    
    def __str__(self):
        return self.srvType