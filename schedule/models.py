from django.db import models


# Create your models here.
class User(models.Model):
    cloudId = models.CharField(max_length=255)


class Schedule(models.Model):
    memberId = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    daysOfWeek = models.JSONField()
    isRecurring = models.BooleanField()
    cloudId = models.ForeignKey(User, on_delete=models.CASCADE, db_column='cloudId')
