# -*- coding: utf-8 -*-
import httplib2
import urllib
from logging import getLogger

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials

logger = getLogger(__name__)

class Client(object):
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

    _flow = None
    _credentials = None
    _service = None

    @property
    def flow(self):
        logger.info('START flow')
        if self._flow is None:
            self._flow = OAuth2WebServerFlow(client_id=self.client_id,
                                             client_secret=self.client_secret,
                                             scope=' '.join(self.scope),
                                             redirect_uri=self.redirect_uri,
                                             prompt='consent')
        logger.info('RETURN %s', '{}'.format(self._flow))
        logger.info('END flow')
        return self._flow

    @property
    def credentials(self):
        logger.info('START credentials')
        if self._credentials is None:
            self._credentials = self._get_credentials_by_token(access_token=self.access_token,
                                                               refresh_token=self.refresh_token,
                                                               token_expiry=self.token_expiry)
        logger.info('RETURN %s', '{}'.format(self._credentials))
        logger.info('END credentials')
        return self._credentials

    @property
    def service(self):
        logger.info('START service')
        if self._service is None:
            http_auth = self.credentials.authorize(httplib2.Http())
            self._service = build('oauth2', 'v2', http=http_auth)
        logger.info('RETURN %s', '{}'.format(self._service))
        logger.info('END service')
        return self._service


    def __init__(self, client_id, client_secret, scope, redirect_uri,
                 access_token=None, refresh_token=None, token_expiry=None):
        logger.info('START __init__')
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri
        logger.info('INPUT self.client_id=%s', self.client_id)
        logger.info('INPUT self.client_secret=%s', self.client_secret)
        logger.info('INPUT self.scope=%s', self.scope)
        logger.info('INPUT self.redirect_uri=%s', self.redirect_uri)

        if None not in (access_token, refresh_token, token_expiry):
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.token_expiry = token_expiry
            logger.info('INPUT self.access_token=%s', self.access_token)
            logger.info('INPUT self.refresh_token=%s', self.refresh_token)
            logger.info('INPUT self.token_expiry=%s', '{}'.format(self.token_expiry))

        logger.info('END __init__')

    def get_auth_uri(self):
        logger.info('START get_auth_uri')
        auth_url = urllib.parse.unquote(self.flow.step1_get_authorize_url())
        logger.info('RETURN %s', auth_url)
        logger.info('END get_auth_uri')
        return auth_url

    def _refresh_access_token(self, credentials):
        logger.info('START refresh_access_token')
        logger.info('INPUT credentials=%s', '{}'.format(credentials))
        if credentials.access_token_expired:
            credentials.refresh(httplib2.Http())
        logger.info('RETURN %s', '{}'.format(credentials))
        logger.info('END refresh_access_token')
        return credentials

    def _get_credentials_by_code(self, code):
        logger.info('START _get_credentials_by_code')
        logger.info('INPUT code=%s', code)
        self._credentials = self._refresh_access_token(self.flow.step2_exchange(code))
        self.access_token = self._credentials.access_token
        self.refresh_token = self._credentials.refresh_token
        self.token_expiry = self._credentials.token_expiry
        logger.info('SET self.access_token=%s', self.access_token)
        logger.info('SET self.refresh_token=%s', self.refresh_token)
        logger.info('SET self.token_expiry=%s', '{}'.format(self.token_expiry))
        logger.info('RETURN %s', '{}'.format(self.credentials))
        logger.info('END _get_credentials_by_code')
        return self.credentials

    def _get_credentials_by_token(self, access_token, refresh_token, token_expiry):
        logger.info('START _get_credentials_by_token')
        logger.info('INPUT access_token=%s, refresh_token=%s, token_expiry=%s',
                    access_token, refresh_token, '{}'.format(token_expiry))
        json = self.CREDENTIALS_JSON_TEMPLATE % {'client_id': self.client_id,
                                                 'client_secret': self.client_secret,
                                                 'access_token': access_token,
                                                 'refresh_token': refresh_token,
                                                 'token_expiry': token_expiry.strftime('%Y-%m-%dT%H:%M:%SZ')}
        logger.info('SET json=%s', json)
        credentials = self._refresh_access_token(OAuth2Credentials.from_json(json))
        logger.info('RETURN %s', '{}'.format(credentials))
        logger.info('END _get_credentials_by_token')
        return credentials

    def get_service(self, code):
        logger.info('START get_service')
        self._get_credentials_by_code(code)
        logger.info('RETURN %s', '{}'.format(self.service))
        logger.info('END get_service')
        return self.service
