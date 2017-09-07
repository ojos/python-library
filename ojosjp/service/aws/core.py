# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from logging import getLogger, INFO

from boto3.session import Session

DEFAULT_REGION = 'ap-northeast-1'

logger = getLogger(__name__)
logger.setLevel(INFO)


def get_client(service_name, aws_access_key_id=None, aws_secret_access_key=None,
               region_name=None):
    logger.info('START get_client')
    logger.info('INPUT service_name=%s, aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s',
                service_name, aws_access_key_id, aws_secret_access_key, region_name)

    region_name = DEFAULT_REGION if region_name is None else region_name
    logger.info('SET region_name=%s', region_name)

    session = Session(aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=_region_name)
    logger.info('SET session=%s', '{}'.format(session.__dict__))

    client = session.client(service_name)

    logger.info('RETURN %s', '{}'.format(client.__dict__))
    logger.info('END get_client')
    return client
