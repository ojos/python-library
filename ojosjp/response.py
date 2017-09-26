# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from logging import getLogger

try:
    import simplejson as json
except ImportError:
    import json

from exception import ResponseException
from misc import now

logger = getLogger(__name__)

def json_response(code, message, **kwargs):
    logger.info('START json_response')
    logger.info('INPUT code=%s, message=%s, kwargs=%s', code, message, kwargs)

    response = {'code': code,
                'message': message,
                'servertime': now()}
    response.update(kwargs)

    logger.info('RETURN %s', response)
    logger.info('END json_response')
    return response


def success(**kwargs):
    logger.info('START success')
    logger.info('INPUT kwargs=%s', kwargs)

    response = json_response(200, 'OK', **kwargs)

    logger.info('RETURN %s', response)
    logger.info('END success')
    return response


def error(code, message):
    logger.info('START error')
    logger.info('INPUT code=%s, message=%s', code, message)

    raise ResponseException(code=code,
                            message=json.dumps(json_response(code, message)))
