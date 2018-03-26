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

from ...decorator import retries
from .core import get_client

logger = getLogger(__name__)


class Ec2(object):
    _client = None

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        logger.info('START __init__')
        logger.info('INPUT aws_access_key_id=%s, aws_secret_access_key=%s, region_name=%s',
                    aws_access_key_id, aws_secret_access_key, region_name)

        self._client = get_client(service_name='ec2',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)

        logger.info('SET self._client=%s', '{}'.format(self._client.__dict__))
        logger.info('END __init__')

    @retries()
    def describe_instances(self, filters, **kwargs):
        res = self._client.describe_instances(Filters=filters, **kwargs)
        return res

    @retries()
    def run_instance(self, image_id, key_name, security_group_ids, subnet_id, tags,
                     minimum=1, maximum=1, instance_type='t2.micro', **kwargs):
        res = self._client.run_instances(ImageId=image_id,
                                         KeyName=key_name,
                                         SecurityGroupIds=security_group_ids,
                                         SubnetId=subnet_id,
                                         TagSpecifications=[{
                                             'ResourceType': 'instance',
                                             'Tags':         tags
                                         }],
                                         MinCount=minimum,
                                         MaxCount=maximum,
                                         InstanceType=instance_type,
                                         **kwargs)
        return res

    @retries()
    def terminate_instances(self, instance_ids, **kwargs):
        res = self._client.terminate_instance(InstanceIds=instance_ids,
                                              **kwargs)
        return res


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

    def __init__(self, client=None, **kwargs):
        logger.info('START __init__')
        logger.info('INPUT client=%s, kwargs=%s', client, kwargs)

        self._client = client if isinstance(client, Ec2) else Ec2()
        self._kwargs = kwargs

        logger.info('END __init__')

    @retries()
    def get_metadata(self, category):
        logger.info('START get_metadata')
        logger.info('INPUT category=%s', category)

        res = requests.get(self.EC2_META_DATA_URL % category,
                           timeout=1)

        logger.info('SET res=%s', '{}'.format(res.__dict__))
        logger.info('RETURN %s', res.text)
        logger.info('END get_metadata')
        return res.text

    def _get_tags(self, instance_id):
        filters = [{'Name': 'instance-id', 'Values': [instance_id]}]
        res = self._client.describe_instances(Filters=filters)

        tags = {t['Key']: t['Value']
                for t in res['Reservations'][0]['Instances'][0]['Tags']}

        return tags
