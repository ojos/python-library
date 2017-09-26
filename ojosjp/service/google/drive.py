# -*- coding: utf-8 -*-
import uuid
from logging import getLogger

from .oauth import Certification
from ...misc import as_tz, time_from_i, time_to_i

logger = getLogger(__name__)

class Drive(Certification):
    SERVICE_NAME = 'drive'
    SERVICE_VERSION = 'v3'
    # https://developers.google.com/identity/protocols/googlescopes#drivev3
    SERVICE_SCOPES = {'drive': 'https://www.googleapis.com/auth/drive',
                      'drive.appdata': 'https://www.googleapis.com/auth/drive.appdata',
                      'drive.file': 'https://www.googleapis.com/auth/drive.file',
                      'drive.metadata': 'https://www.googleapis.com/auth/drive.metadata',
                      'drive.metadata.readonly': 'https://www.googleapis.com/auth/drive.metadata.readonly',
                      'drive.photos.readonly': 'https://www.googleapis.com/auth/drive.photos.readonly',
                      'drive.readonly': 'https://www.googleapis.com/auth/drive.readonly',
                      'drive.scripts': 'https://www.googleapis.com/auth/drive.scripts'}
    # https://developers.google.com/drive/v3/web/mime-types
    SUPPORTED_MIME_TYPES = {'audio': 'application/vnd.google-apps.audio',
                            'document': 'application/vnd.google-apps.document',
                            'drawing': 'application/vnd.google-apps.drawing',
                            'file': 'application/vnd.google-apps.file',
                            'folder': 'application/vnd.google-apps.folder',
                            'form': 'application/vnd.google-apps.form',
                            'fusiontable': 'application/vnd.google-apps.fusiontable',
                            'map': 'application/vnd.google-apps.map',
                            'photo	': 'application/vnd.google-apps.photo	',
                            'presentation': 'application/vnd.google-apps.presentation',
                            'script': 'application/vnd.google-apps.script',
                            'sites': 'application/vnd.google-apps.sites',
                            'spreadsheet': 'application/vnd.google-apps.spreadsheet',
                            'unknown	': 'application/vnd.google-apps.unknown	',
                            'video	': 'application/vnd.google-apps.video	',
                            'drive-sdk': 'application/vnd.google-apps.drive-sdk'}

    _user_id = None
    _permission_id = None

    @property
    def scopes(self):
        logger.info('START scopes')
        if self._scopes is None:
            self._scopes = [self.SERVICE_SCOPES['drive']]
        logger.info('RETURN %s', self._scopes)
        logger.info('END scopes')
        return self._scopes

    @property
    def user_id(self):
        logger.info('START user_id')
        if self._user_id is None:
            self.about()
        logger.info('RETURN %s', self._user_id)
        logger.info('END user_id')
        return self._user_id

    @property
    def permission_id(self):
        logger.info('START permission_id')
        if self._permission_id is None:
            self.about()
        logger.info('RETURN %s', self._permission_id)
        logger.info('END permission_id')
        return self._permission_id

    def about(self):
        logger.info('START about')
        user = self.service.about().get(fields='user').execute()['user']
        self._user_id = user['emailAddress']
        self._permission_id = user['permissionId']
        logger.info('RETURN %s' % user)
        logger.info('END about')
        return user


class Files(object):
    UPLOAD_TYPES = ('media', 'multipart', 'resumable')
    FILE_SPACES = ('drive', 'appDataFolder')

    service = None

    def __init__(self, service):
        self.service = service

    def copy(self, file_id, body):
        return self.service.files().copy(fileId=file_id,
                                         body=body).execute()

    def create(self, upload_type, body):
        return self.service.files().create(fileId=file_id,
                                           uploadType=upload_type,
                                           body=body).execute()

    def empty_trash(self):
        return self.service.files().emptyTrash().execute()

    def export(self, file_id, mime_type):
        return self.service.files().export(fileId=file_id,
                                           mimeType=mime_type).execute()

    def generate_ids(self, count=10, space='drive'):
        return self.service.files().generateIds(count=count,
                                                space=space).execute()

    def get(self, file_id):
        return self.service.files().get(fileId=file_id).execute()

    def list(self, q=None, order_by=None, page_size=100, page_token=None):
        return self.service.files().list().execute()

    def update(self):
        logger.error('Unimplemented')


class Permissions(object):
    PERMISSION_TYPES = ('user', 'group', 'domain', 'anyone')
    PERMISSION_ROLES = ('reader', 'commenter', 'writer', 'owner', 'organizer')

    service = None

    def __init__(self, service):
        self.service = service

    def create(self, file_id, body, send_notification_email=False):
        return self.service.permissions().create(fileId=file_id,
                                                 sendNotificationEmail=send_notification_email,
                                                 body=body).execute()

    def delete(self, file_id, permission_id):
        return self.service.permissions().delete(fileId=file_id,
                                                 permissionId=permission_id).execute()

    def get(self, file_id, permission_id):
        return self.service.permissions().get(fileId=file_id,
                                              permissionId=permission_id).execute()

    def list(self, file_id, page_size=100, page_token=None):
        return self.service.permissions().list(fileId=file_id,
                                               pageSize=page_size,
                                               pageToken=page_token).execute()

    def update(self, file_id, permission_id, body, transfer_ownership=False):
        return self.service.permissions().update(fileId=file_id,
                                                 permissionId=permission_id,
                                                 body=body,
                                                 transferOwnership=transfer_ownership).execute()


class Changes(object):
    DEFAULT_TYPE = 'web_hook'

    _channel_id = None
    _channel_type = None
    _page_token = None

    service = None
    channel_url = None
    file_id = None
    resource_id = None
    expiration = None

    @property
    def channel_id(self):
        logger.info('START channel_id')
        if self._channel_id is None:
            self._channel_id = str(uuid.uuid4())
        logger.info('RETURN %s', self._channel_id)
        logger.info('END channel_id')
        return self._channel_id

    @property
    def page_token(self):
        logger.info('START page_token')
        if self._page_token is None:
            response = self.service.changes().getStartPageToken().execute()
            self._page_token = response['startPageToken']
        logger.info('RETURN %s', self._page_token)
        logger.info('END page_token')
        return self._page_token

    @property
    def channel_type(self):
        logger.info('START channel_type')
        if self._channel_type is None:
            self._channel_type = self.DEFAULT_TYPE
        logger.info('RETURN %s', self._channel_type)
        logger.info('END channel_type')
        return self._channel_type

    def __init__(self, service, channel_id=None, page_token=None, expiration=None, resource_id=None):
        logger.info('START __init__')
        logger.info('INPUT service=%s, channel_id=%s, page_token=%s, expiration=%s',
                    '{}'.format(service.__dict__), channel_id, page_token, expiration)
        self.service = service
        self._channel_id = channel_id
        self._page_token = page_token
        self.expiration = expiration
        self.resource_id = resource_id

        logger.info('END __init__')

    def watch(self, channel_url, file_id=None, channel_type=None):
        logger.info('START watch')
        logger.info('INPUT channel_url=%s, file_id=%s, channel_type=%s',
                    channel_url, file_id, channel_type)
        self.channel_url = channel_url
        self.file_id = file_id
        self._channel_type = channel_type
        expiration = time_to_i(self.expiration, microsecond=True)

        if self.file_id is None:
            response = self.service.changes().watch(pageToken=self.page_token,
                                                    body={'id': self.channel_id,
                                                          'type': self.channel_type,
                                                          'address': self.channel_url,
                                                          'expiration': expiration}).execute()
        else:
            response = self.service.files().watch(fileId=self.file_id,
                                                  body={'id': self.channel_id,
                                                        'type': self.channel_type,
                                                        'address': self.channel_url,
                                                        'expiration': expiration}).execute()
        self.resource_id = response['resourceId']
        logger.info('SET self.resource_id=%s', self.resource_id)
        self.expiration = as_tz(time_from_i(int(response['expiration']), microsecond=True),
                                zone='UTC')
        logger.info('SET self.expiration=%s', self.expiration)
        logger.info('RETURN %s', '{}'.format(response))
        logger.info('END watch')
        return response

    def stop(self, resource_id=None):
        logger.info('START stop')
        if resource_id is None:
            resource_id = self.resource_id
            logger.info('SET resource_id=%s', resource_id)
        response = self.service.channels().stop(body={'id': self.channel_id,
                                                      'resourceId': resource_id}).execute()
        logger.info('RETURN %s', '{}'.format(response))
        logger.info('END stop')

    def list(self, page_token=None):
        logger.info('START list')
        if page_token is None:
            page_token = self.page_token
            logger.info('SET page_token=%s', page_token)
        response = self.service.changes().list(pageToken=page_token).execute()
        self._page_token = response['newStartPageToken']
        logger.info('SET self._page_token=%s', self._page_token)
        logger.info('RETURN %s', response)
        logger.info('END list')
        return response
