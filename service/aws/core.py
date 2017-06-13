# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from boto3.session import Session

def get_client(service_name, aws_access_key_id=None, aws_secret_access_key=None,
               region_name=None):
    _region_name = 'ap-northeast-1' if region_name is None else None
    session = Session(aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=_region_name)
    return session.client(service_name)
