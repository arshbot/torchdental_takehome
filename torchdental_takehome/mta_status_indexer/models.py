from django.conf import settings
from django.db import models
from datetime import timedelta

from django.utils.timezone import now

class Line(models.Model):
    name = models.CharField(max_length=1000, unique=True)

    cached_uptime = models.DurationField(default=timedelta(hours=0))

    @property
    def get_current_uptime(self):
        status = LineUpdate.objects.filter(line=self).order_by('timestamp').last()
        if status == None:
            return None
        elif status:
            return self.cached_uptime + (now() - status.timestamp)
        elif not status:
            return self.cached_uptime

    @property(self):
    def get_total_tracked_time(self):
        first_update = LineUpdate.objects.filter(line=self).order_by('timestamp').first()
        last_update = LineUpdate.objects.filter(line=self).order_by('timestamp').last()

        if last_update == first_update:
            return now() - first_update.timestamp
        else:
            return last_update.timestamp - first_update.timestamp

class LineUpdate(models.Model):

    line = models.ForeignKey(Line, on_delete=models.CASCADE)

    in_service = models.BooleanField()

    timestamp = models.DateTimeField(auto_now_add=True)
