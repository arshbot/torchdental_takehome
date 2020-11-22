import logging, json, requests, time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.db import models
from mta_status_indexer.models import LineUpdate

logger = logging.getLogger(__name__)

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
            #self.process_routes(res['routeDetails'])
            time.sleep(settings.MTA_QUERY_INTERVAL)

    def process_routes(self, routes:list):
        for r in routes:
            self.print_route(r)
            LineUpdate.objects.create(name=r['route'], in_service=r['inService'])

    def print_route(self, route, in_service):
        last_update = LineUpdate.objects.filter(name=route).order_by('timestamp').first()

        if last_update and last_update.in_service and not in_service:
            logger.info('Line {} is experiencing delays'.format(route))
        elif last_update and not last_update.in_service and in_service:
            logger.info('Line {} is now recovered'.format(route))
