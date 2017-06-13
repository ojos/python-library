# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import base64
import hashlib
import hmac

def signature(channel_secret, msg):
    hash = hmac.new(channel_secret.encode('utf-8'),
                    msg.encode('utf-8'),
                    hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    return signature
