# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import json
import time
from logging import getLogger

from ojosjp.decorator import retries
from ojosjp.service.aws.core import get_client

FALID_INVOKE = 'FAILD INVOKE'

logger = getLogger(__name__)

class Lambda(object):
    _client = None

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None, backoff=2):
        logger.info('START __init__')
        logger.info('INPUT aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s, backoff=%s',
                    aws_access_key_id, aws_secret_access_key, region_name, backoff)

        self._backoff = backoff
        self._client = get_client(service_name='lambda',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)

        logger.info('SET self._backoff=%s', self._backoff)
        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')

    @retries()
    def invoke(self, function_name, payload, tries=0, invocation_type='Event'):
        logger.info('START invoke')
        logger.info('INPUT function_name=%s, payload=%s, tries=%s, invocation_type=%s',
                    function_name, payload, tries, invocation_type)

        if tries > 0:
            time.sleep(self._backoff ** (tries - 1))

        payload['tries'] = tries + 1
        res = self._client.invoke(FunctionName=function_name,
                                  InvocationType=invocation_type,
                                  Payload=json.dumps(payload))

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END invoke')
        return res
