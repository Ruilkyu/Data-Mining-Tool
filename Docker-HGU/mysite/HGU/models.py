from django.db import models


# Create your models here.
class hguTest(models.Model):
    name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
