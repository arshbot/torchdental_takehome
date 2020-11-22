from django.conf import settings
from django.db import models

class LineUpdate(models.Model):

    name = models.CharField(max_length=1000)

    in_service = models.BooleanField()

    timestamp = models.DateTimeField()

