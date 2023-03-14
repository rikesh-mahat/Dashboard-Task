from django.db import models
from Models.hosts import Hosts

SOURCE_CODE_OPTIONS = (
 ('OPEN', 'OPEN'),
 ('CLOSE', 'CLOSE'),
 ('IN HOUSE', 'IN HOUSE')
)
SERVER_CONTROL_OPTIONS = (
    ('Subisu', 'Subisu'),
    ('Vendor', 'Vendor'),
    ('Both', 'Both')
)
class Applications(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    devLanguage = models.CharField(max_length=200)
    sourceCode = models.CharField(max_length=200, choices=SOURCE_CODE_OPTIONS)
    serverAccess = models.CharField(max_length=50)
    serverControl = models.CharField(max_length=150, choices=SERVER_CONTROL_OPTIONS)
    hostId = models.ForeignKey(Hosts, on_delete=models.PROTECT, null=True, blank=True)
    
    
    def __str__(self):
        return self.name
    