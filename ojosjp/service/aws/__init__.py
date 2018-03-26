# -*- coding: utf-8 -*-
from .athena import Athena
from .awslambda import Lambda
from .cloudfront import Cloudfront
from .dynamodb import DynamoDB
from .ec2 import InstanceMetadata
from .s3 import S3
from .sns import SNS

__all__ = ['Lambda', 'DynamoDB', 'Ec2', 'InstanceMetadata', 'S3', 'SNS', 'Cloudfront']
