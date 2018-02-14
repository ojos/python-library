# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import json
import time
from logging import getLogger

from ...decorator import retries
from .core import get_client

FALID_INVOKE = 'FAILD INVOKE'

logger = getLogger(__name__)

class Athena(object):
    _client = None

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        logger.info('START __init__')
        logger.info('INPUT aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s',
                    aws_access_key_id, aws_secret_access_key, region_name)

        self._client = get_client(service_name='athena',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)

        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')

    @retries()
    def start_query_execution(self, query, db, output_location):
        logger.info('START start_query_execution')
        logger.info('INPUT query=%s', query)

        res = self._client.start_query_execution(QueryString=query,
                                                 QueryExecutionContext={'Database': db},
                                                 ResultConfiguration={'OutputLocation': 's3://' + output_location})

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END start_query_execution')
        return res

    @retries()
    def get_query_execution(self, execution_id):
        logger.info('START get_query_execution')
        logger.info('INPUT execution_id=%s', execution_id)

        res = self._client.get_query_execution(QueryExecutionId=execution_id)

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END get_query_execution')
        return res

    @retries()
    def get_query_results(self, execution_id):
        logger.info('START get_query_results')
        logger.info('INPUT execution_id=%s', execution_id)

        res = self._client.get_query_results(QueryExecutionId=execution_id)

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END get_query_results')
        return res

    @retries()
    def stop_query_execution(self, execution_id):
        logger.info('START stop_query_execution')
        logger.info('INPUT execution_id=%s', execution_id)

        res = self._client.stop_query_execution(QueryExecutionId=execution_id)

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END stop_query_execution')
        return res
