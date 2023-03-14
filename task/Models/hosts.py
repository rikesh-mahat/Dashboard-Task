from django.db import models

class Hosts(models.Model):
    deviceId = models.IntegerField()
    hostname = models.CharField(max_length=200)
    deviceType = models.CharField(max_length= 200)
    popName = models.CharField(max_length=250)
    popLatitude = models.BigIntegerField()
    pioLatitude = models.BigIntegerField()
    modelName = models.CharField(max_length=250)
    districtname = models.CharField(max_length=250)
    regionName = models.CharField(max_length=250)
    provinceName = models.CharField(max_length=250)
    branchName = models.CharField(max_length=250)
    hyperVisor = models.CharField(max_length=250)
    
    
    def __str__(self):
        return self.hostname