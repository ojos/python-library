#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import copy
import os
import re
import requests
import sys

from logging import getLogger

from botocore.client import BaseClient

from ojosjp.service.aws.core import get_client

DEFAULT_TAGS = {'Name': 'app',
                'Roles': 'app',
                'Environment': 'develop'}
DEFAULT_INSTANCE_ID = 'localhost'
DEFAULT_PUBLIC_IP = '127.0.0.1'

logger = getLogger(__name__)

class InstanceMetadata(object):
    # EC2_USER_DATA_URL = 'http://169.254.169.254/latest/user-data/'
    EC2_META_DATA_URL = 'http://169.254.169.254/latest/meta-data/%s'
    RESOLVE_CONF = '/etc/resolv.conf'

    _once = []
    _client = None
    _instance_id = None
    _public_ip = None
    _tags = None

    @property
    def nameserver(self):
        logger.info('START nameserver')

        with open(self.RESOLVE_CONF, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.find('nameserver') > -1:
                nameserver = line.strip().split(' ')[-1]

        logger.info('RETURN %s', nameserver)
        logger.info('END nameserver')
        return nameserver

    @property
    def instance_id(self):
        logger.info('START instance_id')

        if not 'instance_id' in self._once:
            try:
                self._instance_id = self.get_metadata('instance-id')
                self._once.append('instance_id')
            except:
                pass

        logger.info('RETURN %s', self._instance_id)
        logger.info('END instance_id')
        return self._instance_id

    @property
    def public_ip(self):
        logger.info('START public_ip')

        if not 'public_ip' in self._once:
            try:
                self._public_ip = self.get_metadata('public-ipv4')
                self._once.append('public_ip')
            except:
                pass

        logger.info('RETURN %s', self._public_ip)
        logger.info('END public_ip')
        return self._public_ip

    @property
    def tags(self):
        logger.info('START tags')

        if not 'tags' in self._once:
            try:
                filters = [{'Name': 'instance-id', 'Values': [self.instance_id]}]
                res = self._client.describe_instances(Filters=filters)
                logger.info('SET res=%s', '{}'.format(res))
                self._tags.update({t['Key']: t['Value']
                                   for t in res['Reservations'][0]['Instances'][0]['Tags']})
                self._once.append('tags')
            except:
                pass

        logger.info('RETURN %s', self._tags)
        logger.info('END tags')
        return self._tags

    @property
    def name(self):
        logger.info('START name')

        name = self.tags.get('Name', None)

        logger.info('RETURN %s', name)
        logger.info('END name')
        return name

    @property
    def env(self):
        logger.info('START env')

        env = self.tags.get('Environment', None)

        logger.info('RETURN %s', env)
        logger.info('END env')
        return env

    @property
    def roles(self):
        logger.info('START roles')

        roles = self.tags.get('Roles', '').split(',')

        logger.info('RETURN %s', roles)
        logger.info('END roles')
        return roles


    def __init__(self, client=None,
                       tags=DEFAULT_TAGS,
                       instance_id=DEFAULT_INSTANCE_ID,
                       public_ip=DEFAULT_PUBLIC_IP,
                       timeout=0.5):
        logger.info('START __init__')
        logger.info('INPUT client=%s, tags=%s, instance_id=%s, public_ip=%s, timeout=%s',
                    client, tags, instance_id, public_ip, timeout)

        self._client = client if isinstance(client, BaseClient) else get_client('ec2')
        self._tags = tags
        self._instance_id = instance_id
        self._public_ip = public_ip
        self.timeout = timeout

        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('SET self._tags=%s', self._tags)
        logger.info('SET self._instance_id=%s', self._instance_id)
        logger.info('SET self._public_ip=%s', self._public_ip)
        logger.info('SET self.timeout=%s', self.timeout)
        logger.info('END __init__')

    def get_metadata(self, category):
        logger.info('START get_metadata')
        logger.info('INPUT category=%s', category)

        res = requests.get(self.EC2_META_DATA_URL % category,
                           timeout=self.timeout)

        logger.info('SET res=%s', '{}'.format(res.__dict__))
        logger.info('RETURN %s', res.text)
        logger.info('END get_metadata')
        return res.text
