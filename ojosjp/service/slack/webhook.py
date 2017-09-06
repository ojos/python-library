# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import json
import requests


class Channel(object):

    def __init__(self, url, channel):
        logger.info('START __init__')
        logger.info('INPUT url=%s, channel=%s', url, channel)

        self.url = url
        self.channel = channel

        logger.info('SET self.url=%s', self.url)
        logger.info('SET self.channel=%s', self.channel)
        logger.info('END __init__')

    def incoming(self, text, username=None, icon_emoji=None):
        logger.info('START incoming')
        logger.info('INPUT text=%s, username=%s, icon_emoji=%s',
                    text, username, icon_emoji)

        res = requests.post(self.url, data=json.dumps({'text': text,
                                                       'username': username,
                                                       'icon_emoji': icon_emoji,
                                                       'channel': self.channel}))

        logger.info('SET res=%s', '{}'.format(res.__dict__))
        logger.info('END incoming')
