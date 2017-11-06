# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import base64
import datetime
import pytz
import time

from logging import getLogger

logger = getLogger(__name__)


def time_to_i(dt, microsecond=False):
    logger.info('START time_to_i')
    logger.info('INPUT dt=%s, microsecond=%s', dt, microsecond)

    i = int(time.mktime(dt.timetuple()))
    if microsecond:
        i = i * 1000 + int(dt.microsecond / 1000)

    logger.info('RETURN %s', i)
    logger.info('END time_to_i')
    return i


def time_from_i(i, microsecond=False):
    logger.info('START time_from_i')
    logger.info('INPUT i=%s', i)

    if microsecond:
        i /= 1000
    dt = datetime.datetime.fromtimestamp(i)

    logger.info('RETURN %s', dt)
    logger.info('END time_from_i')
    return dt


def time_from_s(s):
    logger.info('START time_from_s')
    logger.info('INPUT s=%s', s)

    dt = datetime.datetime.strptime(
        s[0:s.find('.')], '%Y-%m-%dT%H:%M:%S')
    tz = s[-5:]
    td = datetime.timedelta(hours=int(tz[:2]),
                            minutes=int(tz[-2:]))
    if s.find('+') > -1:
        dt = dt - td
    else:
        dt = dt + td

    logger.info('RETURN %s', dt)
    logger.info('END time_from_i')
    return dt


def now(microsecond=False):
    logger.info('START now')
    logger.info('INPUT microsecond=%s', microsecond)

    dt = datetime.datetime.now()
    _now = time_to_i(datetime.datetime.now(), microsecond)

    logger.info('RETURN %s', _now)
    logger.info('END now')
    return _now


def as_tz(dt, zone='Asia/Tokyo', base_zone='UTC'):
    logger.info('START as_tz')
    logger.info('INPUT dt=%s, zone=%s, base_zone=%s', dt, zone, base_zone)

    if dt.tzinfo is None:
        dt = pytz.timezone(base_zone).localize(dt)
    dt = dt.astimezone(pytz.timezone(zone))

    logger.info('RETURN %s', dt)
    logger.info('END as_tz')
    return dt


def lazy_loader(name):
    logger.info('START lazy_loader')
    logger.info('INPUT name=%s', name)

    try:
        mod = __import__(name)
    except:
        mod_list = name.split('.')
        mod = __import__('.'.join(mod_list[:-1]))

    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)

    logger.info('RETURN %s', mod)
    logger.info('END lazy_loader')
    return mod
