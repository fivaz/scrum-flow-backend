from django.db import models

from schedule.models import User


class Issue(models.Model):
    isUsed = models.BooleanField(null=True, blank=True)
    estimation = models.FloatField(null=True, blank=True)
    timeSpent = models.IntegerField(null=True, blank=True)
    completedDate = models.DateTimeField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
