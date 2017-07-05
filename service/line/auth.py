# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import base64
import hashlib
import hmac
import requests

def signature(channel_secret, msg):
    hash = hmac.new(channel_secret.encode('utf-8'),
                    msg.encode('utf-8'),
                    hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    return signature

def access_token(client_id, client_secret):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'client_credentials',
               'client_id': client_id,
               'client_secret': client_secret}
    res = requests.post(url, headers=headers, data=payload)
    if res.raise_for_status() is None:
        return res.json()
