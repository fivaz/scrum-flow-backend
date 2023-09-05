from django.db import models


# Create your models here.
class WorkingHours(models.Model):
    start_at = models.TimeField()
    end_at = models.TimeField()
    cloud_id = models.TextField()
