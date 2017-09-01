# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import json
import requests


class Channel(object):

    def __init__(self, url, channel):
        self.url = url
        self.channel = channel

    def incoming(self, text, username=None, icon_emoji=None):
        r = requests.post(self.url, data=json.dumps({'text': text,
                                                     'username': username,
                                                     'icon_emoji': icon_emoji,
                                                     'channel': self.channel}))
