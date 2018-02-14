# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from logging import getLogger

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from ...decorator import retries
from .core import get_client

FALID_INSERT_TO_DYNAMODB = 'FAILD INSERT TO DYNAMODB'
FALID_UPDATE_TO_DYNAMODB = 'FAILD UPDATE TO DYNAMODB'
FALID_GET_TO_DYNAMODB = 'FAILD UPDATE TO DYNAMODB'
FALID_DELETE_TO_DYNAMODB = 'FAILD DELETE TO DYNAMODB'
FALID_SCAN = 'FAILD SCAN'

logger = getLogger(__name__)


class DynamoDB(object):
    _client = None
    _serializer = None
    _deserializer = None

    @property
    def serializer(self):
        logger.info('START serializer')

        if self._serializer is None:
            self._serializer = TypeSerializer()

        logger.info('RETURN %s', self._serializer)
        logger.info('END serializer')

        return self._serializer

    @property
    def deserializer(self):
        logger.info('START deserializer')

        if self._deserializer is None:
            self._deserializer = TypeDeserializer()

        logger.info('RETURN %s', self._deserializer)
        logger.info('END deserializer')

        return self._deserializer

    def __init__(self, table, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        logger.info('START __init__')
        logger.info('INPUT table=%s, aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s',
                    table, aws_access_key_id, aws_secret_access_key, region_name)

        self._table = table
        self._client = get_client(service_name='dynamodb',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)

        logger.info('SET self._table=%s', self._table)
        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')

    @retries()
    def get_item(self, key):
        logger.info('START get_item')
        logger.info('INPUT key=%s', key)

        res = self._client.get_item(TableName=self._table,
                                    Key=self.serializer.serialize(key)['M'])

        res['Item'] = self.deserializer.deserialize({'M': res['Item']})

        logger.info('SET %s', '{}'.format(res))
        logger.info('END get_item')
        return res

    @retries()
    def update_item(self, key, expression, names, values):
        logger.info('START update_item')
        logger.info('INPUT key=%s, expression=%s, names=%s, values=%s',
                    key, expression, names, values)

        res = self._client.update_item(TableName=self._table,
                                       Key=self.serializer.serialize(key)['M'],
                                       UpdateExpression=expression,
                                       ExpressionAttributeNames=names,
                                       ExpressionAttributeValues=self.serializer.serialize(values)[
                                           'M'],
                                       ReturnValues='UPDATED_NEW')

        res['Attributes'] = self.deserializer.deserialize({'M': res['Attributes']})

        logger.info('SET %s', '{}'.format(res))
        logger.info('END update_item')
        return res

    @retries()
    def put_item(self, item):
        logger.info('START put_item')
        logger.info('INPUT item=%s', item)

        res = self._client.put_item(TableName=self._table,
                                    Item=self.serializer.serialize(item)['M'])

        logger.info('SET %s', '{}'.format(res))
        logger.info('END put_item')

    @retries()
    def delete_item(self, item):
        logger.info('START delete_item')
        logger.info('INPUT item=%s', item)

        res = self._client.delete_item(TableName=self._table,
                                       Key=self.serializer.serialize(item)['M'])

        logger.info('SET %s', '{}'.format(res))
        logger.info('END delete_item')

    @retries()
    def scan(self, last_evaludated_key=None, limit=None):
        logger.info('START scan')
        logger.info('INPUT last_evaludated_key=%s, limit=%s', last_evaludated_key, limit)

        kwargs = {'TableName': self._table}
        logger.info('SET %s', kwargs)

        if last_evaludated_key is not None:
            kwargs['ExclusiveStartKey'] = last_evaludated_key
        if limit is not None:
            kwargs['Limit'] = limit

        res = self._client.scan(**kwargs)
        logger.info('SET %s', '{}'.format(res))

        res['Items'] = [self.deserializer.deserialize({'M': item}) for item in res['Items']]

        logger.info('RETURN %s', '{}'.format(res))
        logger.info('END scan')
        return res
