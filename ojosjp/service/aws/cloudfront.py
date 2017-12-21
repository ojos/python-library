# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import json
import time
from logging import getLogger

from ...decorator import retries
from .core import get_client

FALID_INVOKE = 'FAILD INVOKE'

logger = getLogger(__name__)


class Cloudfront(object):
    _client = None

    def __init__(self, distribution_id, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        logger.info('START __init__')
        logger.info('INPUT aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s, distribution_id=%s',
                    aws_access_key_id, aws_secret_access_key, region_name, distribution_id)

        self._distribution_id = distribution_id
        self._client = get_client(service_name='cloudfront',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)

        logger.info('SET self._distribution_id=%s', self._distribution_id)
        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')

    @retries()
    def create_invalidation(self, quantity=None, *items):
        logger.info('START create_invalidation')
        logger.info('INPUT quantity=%s, items=%s', quantity, items)

        invalidation_batch = {
            'Paths': {
                'Quantity': len(items) if quantity is None else quantity,
                'Items': items
            },
            'CallerReference': str(time.time())
        }
        res = self._client.create_invalidation(DistributionId=self._distribution_id,
                                               InvalidationBatch=invalidation_batch)

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END invoke')
        return res
