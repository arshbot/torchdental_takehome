import logging, json, requests, time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.db import models
from mta_status_indexer.models import LineUpdate, Line

logger = logging.getLogger(__name__)

# To silence the logging messages of requests
logging.getLogger("requests").setLevel(logging.WARNING)

class Command(BaseCommand):
    def handle(self, *args, **options):

        mta_url = settings.MTA_URL
        apikey = settings.MTA_API_KEY

        while True:
            response = requests.get(mta_url, params={'apikey':apikey, }) #'updatesSince': something })
            if response.status_code != 200:
                logger.error('MTA endpoint returning error code: {}'.format(response.status_code))
                continue

            res = json.loads(response.content)
            self.process_routes(res['routeDetails'])
            time.sleep(settings.MTA_QUERY_INTERVAL)

    def process_routes(self, routes:list):
        for r in routes:
            route, _ = Line.objects.get_or_create(name=r['route'])
            last_update = route.lineupdate_set.order_by('timestamp').last()

            if not self.is_route_status_different(route, last_update, r['inService']):
                continue

            line_update = LineUpdate.objects.create(line=route, in_service=r['inService'])
            if not line_update.in_service and last_update:
                route.cached_uptime += (line_update.timestamp - last_update.timestamp)

    def is_route_status_different(self, route, last_update, in_service) -> bool:

        if not last_update:
            pass
        elif last_update.in_service and not in_service:
            logger.info('Line {} is experiencing delays'.format(route.name))
        elif not last_update.in_service and in_service:
            logger.info('Line {} is now recovered'.format(route.name))
        elif last_update.in_service == in_service:
            return False

        return True
