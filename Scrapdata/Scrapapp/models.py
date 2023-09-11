import datetime

from django.conf import settings
from django.db import models

# Create your models here.

# scraperapp/models.py
from django.db import models


class ScrapedData(models.Model):
    college_name = models.CharField(max_length=500, default=True)
    PRN = models.CharField(max_length=200, blank=False, default=True)
    name = models.CharField(max_length=255, default=True)
    TcNo = models.IntegerField(default=True)
    date = models.CharField(max_length=100, default=True)
    reason = models.TextField(default=True)
    mobile = models.IntegerField(max_length=10, default=True)

    def __str__(self):
        return self.name
