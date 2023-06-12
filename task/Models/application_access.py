from django.db import models
from Models.staffs import Staffs
from .applications import Applications
from .previliges import Priviliges

APPLICATION_ACCOUNT_OPTIONS =(
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Suspended', 'Suspended')
) 

APPLICATION_ACCESS_OPTIONS = (
    ('Web', 'Web'),
    ('Mobile App', 'Mobile App'),
    ('CLI', 'CLI')
)
class ApplicationAccess(models.Model):
    userId = models.ForeignKey(Staffs, on_delete=models.PROTECT)
    applicationId = models.ForeignKey(Applications, on_delete=models.PROTECT, related_name='user_id')
    applicationUserId = models.IntegerField()
    previligeId = models.ForeignKey(Priviliges, on_delete=models.PROTECT)
    applicationAccountStatus = models.CharField(max_length = 200, choices=APPLICATION_ACCOUNT_OPTIONS)
    applicationAccessMethod = models.CharField(max_length=100, choices=APPLICATION_ACCESS_OPTIONS)
    
    
    