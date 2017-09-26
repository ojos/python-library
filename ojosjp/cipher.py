# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import base64
import pyaes

from logging import getLogger

logger = getLogger(__name__)

def encrypt(key, raw):
    logger.info('START encrypt')
    logger.info('INPUT key=%s, raw=%s', key, raw)

    cipher = pyaes.AESModeOfOperationCTR(key)
    enc = base64.urlsafe_b64encode(cipher.encrypt(raw))

    logger.info('RETURN %s', enc)
    logger.info('END encrypt')
    return enc

def decrypt(key, enc):
    logger.info('START decrypt')
    logger.info('INPUT key=%s, enc=%s', key, enc)

    cipher = pyaes.AESModeOfOperationCTR(key)
    raw = cipher.decrypt(base64.urlsafe_b64decode(enc))

    logger.info('RETURN %s', raw)
    logger.info('END decrypt')
    return raw
