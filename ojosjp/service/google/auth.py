# -*- coding: utf-8 -*-
import httplib2
import urllib
from logging import getLogger

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials

logger = getLogger(__name__)

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

def get_flow(client_id, client_secret, scope, redirect_uri):
    logger.info('START get_flow')
    logger.info('INPUT client_id=%s, client_secret=%s, scope=%s, redirect_uri=%s',
                client_id, client_secret, scope, redirect_uri)
    flow = OAuth2WebServerFlow(client_id=client_id,
                               client_secret=client_secret,
                               scope=' '.join(scope),
                               redirect_uri=redirect_uri,
                               prompt='consent')
    logger.info('RETURN %s', '{}'.format(flow))
    logger.info('END get_flow')
    return flow

def get_auth_uri(flow):
    logger.info('START get_auth_uri')
    logger.info('INPUT flow=%s', flow)
    auth_url = urllib.parse.unquote(flow.step1_get_authorize_url())
    logger.info('RETURN %s', auth_url)
    logger.info('END get_auth_uri')
    return auth_url

def refresh_access_token(credentials):
    logger.info('START refresh_access_token')
    logger.info('INPUT credentials=%s', '{}'.format(credentials))
    if credentials.access_token_expired:
        credentials.refresh(httplib2.Http())
    logger.info('RETURN %s', '{}'.format(credentials))
    logger.info('END refresh_access_token')
    return credentials

def get_credentials_by_code(code):
    logger.info('START get_credentials_by_code')
    logger.info('INPUT code=%s', code)
    flow = get_flow()
    credentials = refresh_access_token(flow.step2_exchange(code))
    logger.info('RETURN %s', '{}'.format(credentials))
    logger.info('END get_credentials_by_code')
    return credentials

def get_credentials_by_token(client_id, client_secret, access_token, refresh_token, token_expiry):
    logger.info('START get_credentials_by_token')
    logger.info('INPUT client_id=%s, client_secret=%s, access_token=%s, refresh_token=%s, token_expiry=%s',
                client_id, client_secret, access_token, refresh_token, '{}'.format(token_expiry))
    json = CREDENTIALS_JSON_TEMPLATE % {'client_id': client_id,
                                        'client_secret': client_secret,
                                        'access_token': access_token,
                                        'refresh_token': refresh_token,
                                        'token_expiry': token_expiry.strftime('%Y-%m-%dT%H:%M:%SZ')}
    logger.info('SET json=%s', json)
    credentials = refresh_access_token(OAuth2Credentials.from_json(json))
    logger.info('RETURN %s', '{}'.format(credentials))
    logger.info('END get_credentials_by_token')
    return credentials

def get_service(credentials):
    logger.info('START get_service')
    http_auth = credentials.authorize(httplib2.Http())
    service = build('oauth2', 'v2', http=http_auth)
    logger.info('RETURN %s', '{}'.format(service))
    logger.info('END get_service')
    return service
