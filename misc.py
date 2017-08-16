# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import base64
import datetime
import time

def time_to_i(dt):
    return int(time.mktime(dt.timetuple()))

def time_from_i(i):
    return datetime.datetime.fromtimestamp(i)

def time_from_s(s):
    dt = datetime.datetime.strptime(
        s[0:s.find('.')], '%Y-%m-%dT%H:%M:%S')
    tz = s[-5:]
    td = datetime.timedelta(hours=int(tz[:2]),
                            minutes=int(tz[-2:]))
    if s.find('+') > -1:
        dt = dt - td
    else:
        dt = dt + td
    return dt

def now(microsecond=False):
    dt = datetime.datetime.now()
    _now = time_to_i(datetime.datetime.now())
    if microsecond:
        _now = int(_now * 1000 + dt.microsecond / 1000)
    return _now

def lazy_loader(name):
    try:
        mod = __import__(name)
    except:
        mod_list = name.split('.')
        mod = __import__('.'.join(mod_list[:-1]))

    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
