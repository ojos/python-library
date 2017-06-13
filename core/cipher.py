# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import base64
import pyaes

def encrypt(key, raw):
    cipher = pyaes.AESModeOfOperationCTR(key.encode('utf-8'))
    return base64.urlsafe_b64encode(cipher.encrypt(raw))

def decrypt(key, enc):
    cipher = pyaes.AESModeOfOperationCTR(key.encode('utf-8'))
    return cipher.decrypt(base64.urlsafe_b64decode(enc))
