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
            self.process_routes(res['routeDetails'])
            time.sleep(settings.MTA_QUERY_INTERVAL)

    def process_routes(self, routes:list):
        for r in routes:
            
            if r['inService']:
                logger.info('{} is currently out of service!'.format(r['route']))
            else:
                logger.info('{} is currently in service!'.format(r['route']))

