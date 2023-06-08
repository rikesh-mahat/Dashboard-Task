from django.db import models
from django.core.exceptions import ValidationError

class Branch(models.Model):
    branch_type = models.CharField(max_length=100, verbose_name='Branch Type')
    address = models.CharField(max_length=200)
    contact = models.BooleanField(default=True, verbose_name='Status')
    longitude = models.FloatField()
    latitude = models.FloatField()
    ip_address = models.GenericIPAddressField()
    remarks = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_type

    def clean(self):
        if self.contact and not self.address:
            raise ValidationError('Contact is true, but no address is provided')