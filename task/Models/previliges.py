from django.db import models

class Priviliges(models.Model):
    preLevel = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    