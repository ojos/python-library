# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals


class ResponseException(Exception):
    code = 500
    message = 'INTERNAL SERVER ERROR'

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])


class BadRequestException(ResponseException):
    code = 400
    message = 'BAD REQUEST'


class UnauthorizedException(ResponseException):
    code = 401
    message = 'UNAUTHORIZED'


class PaymentRequiredException(ResponseException):
    code = 402
    message = 'PAYMENT REQUIRED'


class ForbiddenException(ResponseException):
    code = 403
    message = 'FORBIDDEN'


class NotFoundException(ResponseException):
    code = 404
    message = 'NOT FOUND'


class MethodNotAllowedException(ResponseException):
    code = 405
    message = 'METHOD NOT ALLOW'


class NotAcceptableException(ResponseException):
    code = 406
    message = 'NOT ACCEPTABLE'


class ProxyAuthenticationRequiredException(ResponseException):
    code = 407
    message = 'PROXY AUTHENTICATION REQUIRED'


class RequestTimeoutException(ResponseException):
    code = 408
    message = 'REQUEST TIMEOUT'


class ConflictException(ResponseException):
    code = 409
    message = 'CONFLICT'


class GoneException(ResponseException):
    code = 410
    message = 'GONE'


class LengthRequiredException(ResponseException):
    code = 411
    message = 'LENGTH REQUIRED'


class PreconditionFailedException(ResponseException):
    code = 412
    message = 'PRECONDITION FAILED'


class RequestEntityTooLargeException(ResponseException):
    code = 413
    message = 'REQUEST ENTITY TOO LARGE'


class RequestUriTooLongException(ResponseException):
    code = 414
    message = 'REQUEST-URI TOO LONG'


class UnsupportedMediaTypeException(ResponseException):
    code = 415
    message = 'UNSUPPORTED MEDIA TYPE'


class RequestedRangeNotSatisfiableException(ResponseException):
    code = 416
    message = 'REQUESTED RANGE NOT SATISFIABLE'


class ExpectationFailedException(ResponseException):
    code = 417
    message = 'EXPECTATION FAILED'


class InternalServerErrorException(ResponseException):
    pass


class NotImplementedException(ResponseException):
    code = 501
    message = 'NOT IMPLEMENTED'


class BadGatewayException(ResponseException):
    code = 502
    message = 'BAD GATEWAY'


class ServiceUnavailableException(ResponseException):
    code = 503
    message = 'SERVICE UNAVAILABLE'


class GatewayTimeoutException(ResponseException):
    code = 504
    message = 'GATEWAY TIMEOUT'
