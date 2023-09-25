from django.db import models

from schedule.models import User


# Create your models here.
class Issue(models.Model):
    estimation = models.FloatField(null=True, blank=True)
    timeSpent = models.IntegerField(null=True, blank=True)
    completedDate = models.DateTimeField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
