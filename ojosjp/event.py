# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import copy
from logging import getLogger

logger = getLogger(__name__)


class StaticDispatherMixin(object):
    _event_defaults = {}
    _event_listeners = {}

    @classmethod
    def event_default(cls, event_name, **kwargs):
        if not event_name in cls._event_defaults:
            return False

        cls._event_defaults[event_name] = kwargs

    @classmethod
    def add_listener(cls, event_name, id, func, **kwargs):
        if not event_name in cls._event_defaults:
            return False

        if not event_name in cls._event_listeners:
            cls._event_listeners[event_name] = {}

        _kwargs = copy.deepcopy(cls._event_defaults.get(event_name, {}))
        _kwargs.update(kwargs)

        cls._event_listeners[event_name][id] = {'func': func,
                                                'kwargs': _kwargs}
        return True

    @classmethod
    def remove_listener(cls, event_name, id):
        if not event_name in cls._event_defaults:
            return False

        del cls._event_listeners[event_name][id]
        return True

    @classmethod
    def dispatch_event(cls, event_name, **kwargs):
        for callback in cls._event_listeners[event_name].values():
            _kwargs = copy.deepcopy(callback['kwargs'])
            _kwargs.update(kwargs)
            callback['func'](**_kwargs)

# class ExampleDispatcher(DispatherMixin):
#     _event_defaults = {'hello': {'foo': '_event_defaults.foo', 'bar': '_event_defaults.bar'}}
#
# class EventDispatcherMixin(object):
#     def __init__(cls, name, bases, newattrs):
#         """ Magic needed to create a class with EventDispatcher methods,
#         and an empty callbacks property """
#         super(EventDispatcher, cls).__init__(name, bases, newattrs)
#
#         #cls.emit_event = EventDispatcher.emit_event
#
#         for key, value in EventDispatcher.__dict__.items():
#             if not key.startswith('__'):
#                 if key != "emit_event":
#                     setattr(cls, key, value)
#
#         use_async = has_async and getattr(cls, "async_events", False)
#
#         if use_async:
#             cls.emit_event = asyncio.coroutine(EventDispatcher.async_emit_event)
#         else:
#             cls.emit_event = EventDispatcher.emit_event
#
#     def test_callbacks_dict(self):
#         if not hasattr(self,'callbacks'):
#             self.callbacks = dict()
#
#     def add_listener(self, name, callback, *args, **kwargs):
#         """Adds an event listener on the instance.
#
#         :param name: event name to listen for
#         :type name: unicode or str
#
#         :param callback: the callable to fire when the event is emitted
#         :type callback: callable
#
#         Additionnal args and kwargs are passed to the callback when the event
#         is fired
#
#         If you want to stop the callback chain, your callback should
#         return False. All other return values are discarded.
#         """
#         self.test_callbacks_dict()
#         d = dict(callback=callback, args=args, kwargs=kwargs)
#         self.callbacks.setdefault(name, []).append(d)
#
#     def remove_listener(self, name, func):
#         """
#         Removes a callback from the callback list for the given
#         event name.
#
#         :param name: event name to listen for
#         :type name: unicode or str
#
#         :param func: the function of the callback to unregister
#         :type func: method
#         """
#         self.test_callbacks_dict()
#         if self.callbacks.has_key(name):
#             callbacks = self.callbacks[name]
#             [callbacks.remove(callback) for callback in callbacks if callback['callback'] == func]
#
#     def _prepare_emit_event(self, name, *args, **kwargs):
#         self.test_callbacks_dict()
#         for cbdict in self.callbacks.get(name, list()):
#             handler = cbdict.get('callback')
#
#             listener_args = cbdict.get('args')
#             listener_kwargs = cbdict.get('kwargs')
#
#             myargs = list(args)
#             myargs.extend(listener_args)
#             mykwargs = kwargs
#             mykwargs.update(listener_kwargs)
#
#             yield (handler, myargs, mykwargs)
#
#     def dispatch_event(self, name, *args, **kwargs):
#         """
#         Emit a named event. This will fire all the callbacks registered
#         for the named event.
#
#         :param name: event name to listen for
#         :type name: unicode or str
#
#         Additionnal args and kwargs are passed to the callbacks
#          (before the one that were passed to add_listener).
#         """
#         logger.debug("%s: calling %s with %s and %s" % (repr(self), name,
#                                                     repr(args), repr(kwargs)))
#
#         for handler, hargs, hkwargs in self._prepare_emit_event(name, *args,
#                                                                 **kwargs):
#             result = handler(*hargs, **hkwargs)
#             if result is False:
#                 break
#
#     def async_dispath_event(self, name, *args, **kwargs):
#         """
#         Asynchronously emit a named event.
#         This will fire all the callbacks registered for the named event using
#         a yield from on them.
#
#         :param name: event name to listen for
#         :type name: unicode or str
#
#         Additionnal args and kwargs are passed to the callbacks
#          (before the one that were passed to add_listener).
#
#         Warning: as it is async, it won't stop the event chain on
#         returning False. Also, all event handlers should be async coroutines.
#         """
#         logger.debug("%s: calling %s with %s and %s" % (repr(self), name,
#                                                     repr(args), repr(kwargs)))
#
#         for handler, hargs, hkwargs in self._prepare_emit_event(name, *args,
#                                                                 **kwargs):
#             yield from handler(*hargs, **hkwargs)
