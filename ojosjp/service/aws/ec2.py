#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import copy
import os
import re
import requests
import sys
import time

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
            try:
                self._instance_id = self.get_metadata('instance-id')
            except:
                self._instance_id = self._kwargs.get('instance_id', self.DEFAULT_INSTANCE_ID)

        logger.info('RETURN %s', self._instance_id)
        logger.info('END instance_id')
        return self._instance_id

    @property
    def public_ip(self):
        logger.info('START public_ip')

        if self._public_ip is None:
            try:
                self._public_ip = self.get_metadata('public-ipv4')
            except:
                self._public_ip = self._kwargs.get('public_ip', self.DEFAULT_PUBLIC_IP)

        logger.info('RETURN %s', self._public_ip)
        logger.info('END public_ip')
        return self._public_ip

    @property
    def local_ip(self):
        logger.info('START local_ip')

        if self._local_ip is None:
            try:
                self._local_ip = self.get_metadata('local-ipv4')
            except:
                self._local_ip = self._kwargs.get('local_ip', self.DEFAULT_LOCAL_IP)

        logger.info('RETURN %s', self._local_ip)
        logger.info('END local_ip')
        return self._local_ip

    @property
    def tags(self):
        logger.info('START tags')

        if self._tags is None:
            try:
                self._tags = self._get_tags(self.instance_id)
            except:
                self._tags = self._kwargs.get('tags', self.DEFAULT_TAGS)

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

    def __init__(self, client=None, max_tries=0, **kwargs):
        logger.info('START __init__')
        logger.info('INPUT client=%s, max_tries=%d, kwargs=%s', client, max_tries, kwargs)

        self._client = client if isinstance(client, BaseClient) else get_client('ec2')
        self._max_tries = max_tries
        self._kwargs = kwargs

        logger.info('END __init__')

    def get_metadata(self, category):
        logger.info('START get_metadata')
        logger.info('INPUT category=%s', category)

        timeout = 1
        tries = 0
        while True:
            try:
                res = requests.get(self.EC2_META_DATA_URL % category,
                                   timeout=timeout)
                break
            except Exception as e:
                timeout *= 2
                tries += 1
                if self._max_tries != 0 and tries >= self._max_tries:
                    raise e

        logger.info('SET res=%s', '{}'.format(res.__dict__))
        logger.info('RETURN %s', res.text)
        logger.info('END get_metadata')
        return res.text

    def _get_tags(self, instance_id):
        filters = [{'Name': 'instance-id', 'Values': [instance_id]}]
        timeout = 1
        tries = 0
        while True:
            try:
                res = self._client.describe_instances(Filters=filters)
                logger.info('SET res=%s', '{}'.format(res))
                break
            except Exception as e:
                time.sleep(timeout)
                timeout *= 2
                tries += 1
                if self._max_tries != 0 and tries >= self._max_tries:
                    raise e

        tags = {t['Key']: t['Value']
                for t in res['Reservations'][0]['Instances'][0]['Tags']}

        return tags
