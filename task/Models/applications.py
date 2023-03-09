from django.db import models


class Applications(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    devLanguage = models.CharField(max_length=200)
    sourceCode = models.CharField(max_length=200)
    serverAccess = models.CharField(max_length=50)
    serverControl = models.CharField(max_length=150)
    