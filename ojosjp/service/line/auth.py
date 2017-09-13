# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import base64
import hashlib
import hmac
import requests

from logging import getLogger

logger = getLogger(__name__)

OAUTH_URL = 'https://api.line.me/v2/oauth/accessToken'

def signature(channel_secret, msg):
    logger.info('START signature')
    logger.info('INPUT channel_secret=%s, msg=%s', channel_secret, msg)

    hash = hmac.new(channel_secret.encode('utf-8'),
                    msg.encode('utf-8'),
                    hashlib.sha256).digest()
    signature = base64.b64encode(hash)

    logger.info('RETURN %s', signature)
    logger.info('END signature')
    return signature

def access_token(client_id, client_secret):
    logger.info('START access_token')
    logger.info('INPUT client_id=%s, client_secret=%s', client_id, client_secret)

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'client_credentials',
               'client_id': client_id,
               'client_secret': client_secret}
    logger.info('SET headers=%s', headers)
    logger.info('SET payload=%s', payload)

    res = requests.post(OAUTH_URL, headers=headers, data=payload)
    logger.info('SET res=%s', '{}'.format(res.__dict__))

    if res.raise_for_status() is None:
         access_token = res.json()

    logger.info('RETURN %s', access_token)
    logger.info('END access_token')
    return access_token
