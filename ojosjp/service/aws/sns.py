# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import datetime
import json
import sys
import traceback

from logging import getLogger

from ...misc import time_from_i
from .core import get_client

logger = getLogger(__name__)

class SNS(object):
    ERROR_SUBJECT = 'ERROR : %(resource_path)s %(code)s %(message)s'
    ERROR_BODY = '''
timestamp : %(timestamp)s
stage : %(stage)s
resource path : %(resource_path)s
source ip : %(source_ip)s
user agent : %(user_agent)s
trackback : %(trackback)s
request headers : %(headers)s
request body : %(body)s
'''
    MISSED_SUBJECT = 'MISSED : %(code)s %(message)s'
    MISSED_BODY = '''
timestamp : %(timestamp)s
trackback : %(trackback)s
kwargs : %(kwargs)s
'''

    _arn = None

    def __init__(self, arn, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        logger.info('START __init__')
        logger.info('INPUT arn=%s, aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s',
                    arn, aws_access_key_id, aws_secret_access_key, region_name)

        self._arn = arn
        self._client = get_client(service_name='sns',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)

        logger.info('SET self._arn=%s', self._arn)
        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')


    def traceback_info(self):
        logger.info('START traceback_info')

        tbinfo = traceback.format_tb(sys.exc_info()[2])
        info = ' '.join(tbinfo).strip()

        logger.info('SET tbinfo=%s', '{}'.format(tbinfo.__dict__))
        logger.info('RETURN %s', info)
        logger.info('END traceback_info')
        return info

    def publish(self, subject, message):
        logger.info('START publish')
        logger.info('INPUT subject=%s, message=%s', subject, message)

        res = self._client.publish(TargetArn=self._arn,
                                   Subject=subject,
                                   Message=message)

        logger.info('SET res=%s', '{}'.format(res))
        logger.info('END publish')

    def miss(self, code, message, **kwargs):
        logger.info('START miss')
        logger.info('INPUT code=%s, message=%s, kwargs=%s', code, message, kwargs)

        jst_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        logger.info('SET jst_dt=%s', '{}'.format(jst_dt.__dict__))

        self.publish(subject=self.MISSED_SUBJECT % {'code': code,
                                                    'message': message},
                     message=self.MISSED_BODY % {'timestamp': jst_dt.strftime('%Y-%m-%dT%H:%M:%S+09:00'),
                                                 'trackback': self.traceback_info(),
                                                 'kwargs': json.dumps(kwargs)})

        logger.info('END miss')

    def error(self, exception, event):
        logger.info('START error')
        logger.info('INPUT exception=%s, event=%s', '{}'.format(exception.__dict__), kwargs)

        response = json.loads(exception.message)
        logger.info('SET response=%s', response)
        jst_dt = time_from_i(response['servertime']) + datetime.timedelta(hours=9)
        logger.info('SET jst_dt=%s', '{}'.format(jst_dt.__dict__))
        body = json.dumps(event['body']) if isinstance(event['body'], dict) else event['body']
        logger.info('SET body=%s', body)

        self.publish(subject=self.ERROR_SUBJECT % {'resource_path': event['resource_path'],
                                                   'code': response['code'],
                                                   'message': response['message']},
                     message=self.ERROR_BODY % {'timestamp': jst_dt.strftime('%Y-%m-%dT%H:%M:%S+09:00'),
                                                'stage': event['stage'],
                                                'source_ip': event['source_ip'],
                                                'resource_path': event['resource_path'],
                                                'user_agent': event['user_agent'],
                                                'trackback': self.traceback_info(),
                                                'headers': json.dumps(event['headers']),
                                                'body': body})

        logger.info('END error')
