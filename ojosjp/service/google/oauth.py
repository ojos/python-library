# -*- coding: utf-8 -*-
import httplib2
import urllib
from logging import getLogger

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials

from ...event import StaticDispatherMixin

logger = getLogger(__name__)

class Certification(object):
    CREDENTIALS_JSON_TEMPLATE =\
        ('{'
         '"_module": "oauth2client.client",'
         '"token_expiry": "%(token_expiry)s",'
         '"access_token": "%(access_token)s",'
         '"token_uri": "https://accounts.google.com/o/oauth2/token",'
         '"invalid": false,'
         '"token_response": {'
         '"access_token": "%(access_token)s",'
         '"token_type": "Bearer",'
         '"expires_in": 3595'
         '},'
         '"client_id": "%(client_id)s",'
         '"id_token": null,'
         '"client_secret": "%(client_secret)s",'
         '"revoke_uri": "https://accounts.google.com/o/oauth2/revoke",'
         '"_class": "OAuth2Credentials",'
         '"refresh_token": "%(refresh_token)s",'
         '"user_agent": null'
         '}')
    SERVICE_NAME = 'oauth2'
    SERVICE_VERSION = 'v2'
    # https://developers.google.com/identity/protocols/googlescopes#oauth2v2
    SERVICE_SCOPES = {'plus.login': 'https://www.googleapis.com/auth/plus.login',
                      'plus.me': 'https://www.googleapis.com/auth/plus.me',
                      'userinfo.email': 'https://www.googleapis.com/auth/userinfo.email',
                      'userinfo.profile': 'https://www.googleapis.com/auth/userinfo.profile'}

    _flow = None
    _service = None
    _service_name = None
    _service_version = None
    _scopes = None
    _credentials = None

    @classmethod
    def get_by_code(cls, code, client_id, client_secret, redirect_uri):
        logger.info('START get_by_code')
        certification = cls(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri)
        logger.info('SET certification=%s', '{}'.format(certification.__dict__))
        certification.get_credentials_by_code(code)

        logger.info('RETURN %s', '{}'.format(certification))
        logger.info('END get_by_code')
        return certification

    @property
    def flow(self):
        logger.info('START flow')
        if self._flow is None:
            self._flow = OAuth2WebServerFlow(client_id=self.client_id,
                                             client_secret=self.client_secret,
                                             redirect_uri=self.redirect_uri,
                                             scope=' '.join(self.scopes),
                                             prompt='consent')
        logger.info('RETURN %s', '{}'.format(self._flow))
        logger.info('END flow')
        return self._flow

    @property
    def service(self):
        logger.info('START service')
        if self._service is None:
            http_auth = self._credentials.authorize(httplib2.Http())
            self._service = build(self.service_name, self.service_version,
                                  http=http_auth,
                                  cache_discovery=False)
        logger.info('RETURN %s', '{}'.format(self._service))
        logger.info('END service')
        return self._service

    @property
    def service_name(self):
        logger.info('START service_name')
        if self._service_name is None:
            self._service_name = self.SERVICE_NAME
        logger.info('RETURN %s', self._service_name)
        logger.info('END service_name')
        return self._service_name

    @property
    def service_version(self):
        logger.info('START service_version')
        if self._service_version is None:
            self._service_version = self.SERVICE_VERSION
        logger.info('RETURN %s', self._service_version)
        logger.info('END service_version')
        return self._service_version

    @property
    def scopes(self):
        logger.info('START scopes')
        if self._scopes is None:
            self._scopes = list(self.SERVICE_SCOPES.values())
        logger.info('RETURN %s', self._scopes)
        logger.info('END scopes')
        return self._scopes

    @property
    def access_token(self):
        return self._credentials.access_token

    @property
    def refresh_token(self):
        return self._credentials.refresh_token

    @property
    def token_expiry(self):
        return self._credentials.token_expiry.strftime('%Y-%m-%dT%H:%M:%SZ')

    def __init__(self, client_id, client_secret, redirect_uri,
                 access_token=None, refresh_token=None, token_expiry=None, **kwargs):
        logger.info('START __init__')
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        logger.info('INPUT self.client_id=%s', self.client_id)
        logger.info('INPUT self.client_secret=%s', self.client_secret)
        logger.info('INPUT self.redirect_uri=%s', self.redirect_uri)

        for key, value in kwargs.items():
            setattr(self, '_%s' % key, value)
            logger.info('INPUT self._%s=%s', key, value)

        if None not in (access_token, refresh_token, token_expiry):
            self.get_credentials_by_token(access_token=access_token,
                                          refresh_token=refresh_token,
                                          token_expiry=token_expiry)

        logger.info('END __init__')

    def get_auth_uri(self):
        logger.info('START get_auth_uri')
        auth_url = urllib.parse.unquote(self.flow.step1_get_authorize_url())
        logger.info('RETURN %s', auth_url)
        logger.info('END get_auth_uri')
        return auth_url

    def get_credentials_by_code(self, code):
        logger.info('START get_credentials_by_code')
        logger.info('INPUT code=%s', code)
        self._credentials = self.flow.step2_exchange(code)
        logger.info('END get_credentials_by_code')

    def refresh_credentials(self):
        logger.info('START refresh_credentials')
        is_refresh = False
        if self._credentials.access_token_expired:
            self._credentials.refresh(httplib2.Http())
            is_refresh = True
        logger.info('RETURN %s', is_refresh)
        logger.info('END refresh_credentials')
        return is_refresh

    def get_credentials_by_token(self, access_token, refresh_token, token_expiry):
        logger.info('START get_credentials_by_token')
        logger.info('INPUT access_token=%s, refresh_token=%s, token_expiry=%s',
                    access_token, refresh_token, '{}'.format(token_expiry))
        json = self.CREDENTIALS_JSON_TEMPLATE % {'client_id': self.client_id,
                                                 'client_secret': self.client_secret,
                                                 'access_token': access_token,
                                                 'refresh_token': refresh_token,
                                                 'token_expiry': token_expiry}
        logger.info('SET json=%s', json)
        self._credentials = OAuth2Credentials.from_json(json)
        self.refresh_credentials()
        logger.info('END get_credentials_by_token')
