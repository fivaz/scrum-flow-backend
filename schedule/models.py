from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class User(models.Model):
    cloudId = models.CharField(max_length=255)


class Schedule(models.Model):
    memberId = models.CharField(max_length=255)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    freq = models.CharField(max_length=200, null=True, blank=True)
    byweekday = ArrayField(models.CharField(max_length=3), null=True, blank=True)
    dtstart = models.DateTimeField(null=True, blank=True)
    until = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
