# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

class ServiceException(Exception):
  message = 'Error'

  def __init__(self, **kwargs):
      for key in kwargs.keys():
          setattr(self, key, kwargs[key])
