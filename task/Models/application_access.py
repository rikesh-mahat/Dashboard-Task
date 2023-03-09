from django.db import models
from .employees import Employees
from .applications import Applications
from .previliges import Priviliges
class ApplicationAccess(models.Model):
    userId = models.ForeignKey(Employees, on_delete=models.PROTECT)
    applicationId = models.ForeignKey(Applications, on_delete=models.PROTECT, related_name='user_id')
    applicationUserId = models.ForeignKey(Employees, on_delete=models.PROTECT,related_name='application_id')
    previligeId = models.ForeignKey(Priviliges, on_delete=models.PROTECT)
    applicationAccountStatus = models.BooleanField(default = True)
    applicationAccessMethod = models.IntegerField(default=0)