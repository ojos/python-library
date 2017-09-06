# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import time

from logging import getLogger, INFO

logger = getLogger(__name__)
logger.setLevel(INFO)

def retry_handler(tries_remaining, exception, delay):
    logger.warning("Caught '%s', %d tries remaining, sleeping for %s seconds",
                   exception, tries_remaining, delay)


def retries(max_tries=3, delay=1, backoff=2, exceptions=(Exception,), hook=retry_handler):
    def dec(func):
        def f2(*args, **kwargs):
            mydelay = delay
            tries = range(max_tries)
            tries.reverse()
            for tries_remaining in tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        if hook is not None:
                            hook(tries_remaining, e, mydelay)
                        time.sleep(mydelay)
                        mydelay = mydelay * backoff
                    else:
                        raise
                else:
                    break
        return f2
    return dec

def error_catch(error_func, exception=(Exception,)):
    def _error_response(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except exceptions as e:
                logger.exception('Error %s', e)
                return error_func(exception)
        return wrapper
    return _error_response
