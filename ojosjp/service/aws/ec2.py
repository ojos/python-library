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

from .core import get_client


logger = getLogger(__name__)


class InstanceMetadata(object):
    # EC2_USER_DATA_URL = 'http://169.254.169.254/latest/user-data/'
    EC2_META_DATA_URL = 'http://169.254.169.254/latest/meta-data/%s'
    RESOLVE_CONF = '/etc/resolv.conf'
    DEFAULT_TAGS = {'Name': 'app',
                    'Roles': 'app',
                    'Environment': 'develop'}
    DEFAULT_INSTANCE_ID = 'localhost'
    DEFAULT_PUBLIC_IP = '127.0.0.1'
    DEFAULT_LOCAL_IP = '0.0.0.0'

    _client = None
    _instance_id = None
    _public_ip = None
    _local_ip = None
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

        if self._instance_id is None:
            if self._mock:
                self._instance_id = kwargs.get('instance_id', self.DEFAULT_INSTANCE_ID)
            else:
                self._instance_id = self.get_metadata('instance-id')

        logger.info('RETURN %s', self._instance_id)
        logger.info('END instance_id')
        return self._instance_id

    @property
    def public_ip(self):
        logger.info('START public_ip')

        if self._public_ip is None:
            if self._mock:
                self._public_ip = kwargs.get('public_ip', self.DEFAULT_PUBLIC_IP)
            else:
                self._public_ip = self.get_metadata('public-ipv4')

        logger.info('RETURN %s', self._public_ip)
        logger.info('END public_ip')
        return self._public_ip

    @property
    def local_ip(self):
        logger.info('START local_ip')

        if self._local_ip is None:
            if self._mock:
                self._local_ip = kwargs.get('local_ip', self.DEFAULT_LOCAL_IP)
            else:
                self._local_ip = self.get_metadata('local-ipv4')

        logger.info('RETURN %s', self._local_ip)
        logger.info('END local_ip')
        return self._local_ip

    @property
    def tags(self):
        logger.info('START tags')

        if self._tags is None:
            if self._mock:
                self._tags = kwargs.get('tags', self.DEFAULT_TAGS)
            else:
                self._tags = self._get_tags(self.instance_id)

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

    def __init__(self, client=None, mock=False, **kwargs):
        logger.info('START __init__')
        logger.info('INPUT client=%s, mock=%s, kwargs=%s', client, mock, kwargs)

        self._client = client if isinstance(client, BaseClient) else get_client('ec2')
        self._mock = mock
        self._kwargs = kwargs

        logger.info('END __init__')

    def get_metadata(self, category):
        logger.info('START get_metadata')
        logger.info('INPUT category=%s', category)

        try:
            res = requests.get(self.EC2_META_DATA_URL % category)
        except Exception:
            time.sleep(1)
            res = self.get_metadata(category)

        logger.info('SET res=%s', '{}'.format(res.__dict__))
        logger.info('RETURN %s', res.text)
        logger.info('END get_metadata')
        return res.text

    def _get_tags(self, instance_id):
        try:
            filters = [{'Name': 'instance-id', 'Values': [instance_id]}]
            res = self._client.describe_instances(Filters=filters)
            logger.info('SET res=%s', '{}'.format(res))
            tags = {t['Key']: t['Value']
                    for t in res['Reservations'][0]['Instances'][0]['Tags']}
        except Exception:
            time.sleep(1)
            tags = self._get_tags(instance_id)

        return tags
