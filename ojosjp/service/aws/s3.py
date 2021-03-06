# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import gzip

from logging import getLogger

try:
    from io import BytesIO
except ImportError:
    from BytesIO import BytesIO

from ...decorator import retries
from .core import get_client

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
        return obj

    @retries()
    def get_text(self, key):
        logger.info('START get_text')

        obj = self.get_object(key=key)
        body = obj['Body'].read()
        content_encoding = obj.get('ContentEncoding', None)
        if content_encoding == 'gzip':
            text = self._expand_text(body)
        else:
            text = body

        logger.info('RETURN %s', text)
        logger.info('END get_text')
        return text.decode()

    def _expand_text(self, text):
        logger.info('START _expand_text')
        logger.info('INPUT text=%s', text)

        bytesio = BytesIO(text)
        gzip_file = gzip.GzipFile(fileobj=bytesio, mode='rb')
        text = gzip_file.read()
        gzip_file.close()

        logger.info('RETURN %s', text)
        logger.info('END _expand_text')
        return text

    def _compress_text(self, context):
        logger.info('START _compress_text')
        logger.info('INPUT context=%s', context)

        bytesio = BytesIO()
        gzip_file = gzip.GzipFile(fileobj=bytesio, mode='wb')
        gzip_file.write(context.encode('utf-8'))
        gzip_file.close()
        context = bytesio.getvalue()

        logger.info('RETURN %s', context)
        logger.info('END _compress_text')
        return context

    @retries()
    def put_object(self, key, body, content_type, cache_control=None, acl=S3_ACL, compress=False, **kwargs):
        logger.info('START put_object')
        logger.info('INPUT key=%s, body=%s, content_type=%s, cache_control=%s, acl=%s, compress=%s',
                    key, body, content_type, cache_control, acl, compress)

        kwargs.update({'Bucket': self._bucket,
                       'ACL': acl,
                       'ContentType': content_type,
                       'Key': key,
                       'Body': body})
        if cache_control is not None:
            kwargs['CacheControl'] = cache_control
        logger.info('SET kwargs=%s', kwargs)

        if compress:
            kwargs['Body'] = self._compress_text(kwargs['Body'])
            kwargs['ContentEncoding'] = 'gzip'
        res = self._client.put_object(**kwargs)

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END put_object')
        return res

    @retries()
    def copy(self, source_key, target_key, acl=S3_ACL):
        logger.info('START copy')
        logger.info('INPUT source_key=%s, target_key=%s', source_key, target_key)

        res = self._client.copy(CopySource={'Bucket': self._bucket,
                                            'Key': source_key},
                                Bucket=self._bucket,
                                Key=target_key,
                                ExtraArgs={'ACL': acl})

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END copy')
        return res

    @retries()
    def delete_object(self, key):
        logger.info('START delete_object')

        obj = self._client.delete_object(Bucket=self._bucket,
                                         Key=key)

        logger.info('RETURN %s', '{}'.format(obj))
        logger.info('END delete_object')
        return obj
