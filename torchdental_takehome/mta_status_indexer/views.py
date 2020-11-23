from datetime import timedelta
from django.db.models.functions import datetime
from django.http import JsonResponse, HttpResponseNotFound

from mta_status_indexer.models import LineUpdate

def status(request, line):
    last_update = Line.objects.filter(name=line).line_updates.order_by('timestamp').last()
    if not last_update:
        return HttpResponseNotFound()
    return JsonResponse({'status': last_update.in_service})

def uptime_percentage(request, line):
    line = Line.objects.filter(name=line).first()
    last_update = line.line_updates.order_by('timestamp').last()

    if not line:
        return HttpResponseNotFound()
    return JsonResponse({'current_uptime': line.get_current_uptime / line.get_total_tracked_time})



    """
    line_updates = LineUpdate.objects.filter('line').order_by('timestamp')

    if line_updates.count == 0:
        # return we don't know
        pass
    elif line_updates.count == 1:
        # either 1 or 0 depending on if up
        pass
    down_time = timedelta(hours=0)
    now = datetime.now()
    total_time = line_updates.last().timestamp - line_updates.first().timestamp + now

    i = 0
    while i < line_updates.count:
        if line_updates[i].in_service and i == line_updates.count-1:
            down_time += now - line_updates[i].timestamp
        elif line_updates[i].in_service:
            down_time += line_updates[i+1].timestamp - line_updates[i].timestamp
            i+=2
        else:
            i+=1
            """
