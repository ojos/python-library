# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import gzip

from logging import getLogger

try:
    from io import BytesIO
except ImportError:
    from BytesIO import BytesIO

from ojosjp.decorator import retries
from ojosjp.service.aws.core import get_client

FALID_GET_OBJECT = 'FAILD GET OBJECT'
FAILD_PUT_OBJECT = 'FAILD PUT OBJECT'
FALID_COPY_OBJECT = 'FAILD COPY'

logger = getLogger(__name__)

class S3(object):
    S3_ACL = 'public-read'

    _client = None
    _bucket = None

    def __init__(self, bucket, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        logger.info('START __init__')
        logger.info('INPUT bucket=%s, aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s',
                    bucket, aws_access_key_id, aws_secret_access_key, region_name)

        self._bucket = bucket
        self._client = get_client(service_name='s3',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)

        logger.info('SET self._bucket=%s', self._bucket)
        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')


    @retries()
    def get_object(self, key):
        logger.info('START get_object')

        obj = self._client.get_object(Bucket=self._bucket,
                                      Key=key)

        logger.info('RETURN %s', '{}'.format(obj))
        logger.info('END get_object')

    def _expand_text(self, context):
        logger.info('START _expand_text')
        logger.info('INPUT context=%s', '{}'.format(context.__dict__))

        bytesio = BytesIO(context)
        gzip_file = gzip.GzipFile(fileobj=bytesio, mode='rb')
        context = gzip_file.read()
        gzip_file.close()

        logger.info('RETURN %s', context)
        logger.info('END _expand_text')
        return context

    def _compress_text(self, context):
        logger.info('START _compress_text')
        logger.info('INPUT context=%s', context)

        bytesio = BytesIO()
        gzip_file = gzip.GzipFile(fileobj=bytesio, mode='wb')
        gzip_file.write(context)
        gzip_file.close()
        context = bytesio.getvalue()

        logger.info('RETURN %s', '{}'.format(context.__dict__))
        logger.info('END _compress_text')
        return context

    @retries()
    def put_object(self, key, body, content_type, cache_control, acl=S3_ACL, compress=False):
        logger.info('START put_object')
        logger.info('INPUT key=%s, body=%s, content_type=%s, cache_control=%s, acl=%s, compress=%s',
                    key, body, content_type, cache_control, acl, compress)

        kwargs = {'Bucket': self._bucket,
                  'ACL': acl,
                  'ContentType': content_type,
                  'CacheControl': cache_control,
                  'Key': key,
                  'Body': body}
        logger.info('SET kwargs=%s', kwargs)

        if compress:
            kwargs['Body'] = self._compress_text(kwargs['Body'])
            kwargs['ContentEncoding'] = 'gzip'
        res = self._client.put_object(**kwargs)

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END put_object')
        return res

    @retries()
    def copy(self, source_key, target_key):
        logger.info('START put_object')
        logger.info('INPUT source_key=%s, target_key=%s', source_key, target_key)

        res = self._client.copy(CopySource={'Bucket': self._bucket,
                                      'Key': source_key},
                                Bucket=self._bucket,
                                Key=target_key)

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END put_object')
        return res
