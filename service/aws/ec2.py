#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import copy
import os
import re
import requests
import sys

from service.aws.core import get_client


DEFAULT_TAGS = {'Name': 'app',
                'Roles': 'app',
                'Environment': 'develop'}
DEFAULT_INSTANCE_ID = 'localhost'
DEFAULT_PUBLIC_IP = '127.0.0.1'

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
        with open(self.RESOLVE_CONF, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.find('nameserver') > -1:
                return line.strip().split(' ')[-1]

    @property
    def instance_id(self):
        if not 'instance_id' in self._once:
            try:
                self._instance_id = self.get_metadata('instance-id')
                self._once.append('instance_id')
            except:
                pass
        return self._instance_id

    @property
    def public_ip(self):
        if not 'public_ip' in self._once:
            try:
                self._public_ip = self.get_metadata('public-ipv4')
                self._once.append('public_ip')
            except:
                pass
        return self._public_ip

    @property
    def tags(self):
        if not 'tags' in self._once:
            try:
                filters = [{'Name': 'instance-id', 'Values': [self.instance_id]}]
                res = self._client.describe_instances(Filters=filters)
                self._tags.update({t['Key']: t['Value']
                                   for t in res['Reservations'][0]['Instances'][0]['Tags']})
                self._once.append('tags')
            except:
                pass

        return self._tags

    @property
    def name(self):
        return self.tags.get('Name', None)

    @property
    def env(self):
        return self.tags.get('Environment', None)

    @property
    def roles(self):
        return self.tags.get('Roles', '').split(',')


    def __init__(self, client=None,
                       tags=DEFAULT_TAGS,
                       instance_id=DEFAULT_INSTANCE_ID,
                       public_ip=DEFAULT_PUBLIC_IP,
                       timeout=0.5):
        if client is None:
            client = get_client('ec2')
        self._client = client

        self._tags = tags
        self._instance_id = instance_id
        self._public_ip = public_ip
        self.timeout = timeout

    def get_metadata(self, category):
        res = requests.get(self.EC2_META_DATA_URL % category,
                           timeout=self.timeout)
        return res.text
