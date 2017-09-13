# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from logging import getLogger

from linebot import HttpClient, LineBotApi, RequestsHttpClient
from linebot.exceptions import LineBotApiError

from ojosjp.decorator import retries

logger = getLogger(__name__)

class Messaging(object):
    _client = None

    def __init__(self, channel_access_token, endpoint=LineBotApi.DEFAULT_API_ENDPOINT,
                 timeout=HttpClient.DEFAULT_TIMEOUT, http_client=RequestsHttpClient):
        logger.info('START __init__')
        logger.info('INPUT channel_access_token=%s, endpoint=%s, timeout=%s, http_client=%s',
                    channel_access_token, endpoint, timeout, http_client)

        self._client = LineBotApi(channel_access_token, endpoint, timeout, http_client)
        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')


    @retries()
    def reply_message(self, reply_token, messages, timeout=None):
        logger.info('START reply_message')
        logger.info('INPUT reply_token=%s, messages=%s, timeout=%s',
                    reply_token, messages, timeout)

        res = self._client.reply_message(reply_token, messages)

        logger.info('SET res=%s', '{}'.format(res))
        logger.info('END reply_message')

    @retries()
    def push_message(self, to, messages, timeout=None):
        logger.info('START push_message')
        logger.info('INPUT to=%s, messages=%s, timeout=%s', to, messages, timeout)

        res = self._client.push_message(to, messages)

        logger.info('SET res=%s', '{}'.format(res))
        logger.info('END push_message')
