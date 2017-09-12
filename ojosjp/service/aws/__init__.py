# -*- coding: utf-8 -*-
from .awslambda import Lambda
from .dynamodb import DynamoDB
from .ec2 import InstanceMetadata
from .s3 import S3
from .sns import SNS

__all__ = ['Lambda', 'DynamoDB', 'InstanceMetadata', 'S3', 'SNS']
