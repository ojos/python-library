# -*- coding: utf-8 -*-
import uuid
from logging import getLogger

from .oauth import Certification

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

    @property
    def scopes(self):
        logger.info('START scopes')
        if self._scopes is None:
            self._scopes = [self.SERVICE_SCOPES['drive']]
        logger.info('RETURN %s', self._scopes)
        logger.info('END scopes')
        return self._scopes

    def about(self):
        return self.service.about().get(fields='user').execute()['user']


class File(object):
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

    def list(self, file_id):
        return self.service.files().get(fileId=file_id).execute()

    def update(self):
        logger.error('Unimplemented')


class Permission(object):
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


class Channel(object):
    DEFAULT_TYPE = 'web_hook'

    _channel_id = None
    _channel_type = None
    _page_token = None

    service = None
    channel_address = None
    file_id = None
    resource_id = None

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

    def __init__(self, service, channel_address, file_id=None, channel_id=None, channel_type=None):
        self.service = service
        self.channel_address = channel_address
        self.file_id = file_id
        self._channel_id = channel_id
        self._channel_type = channel_type

        if self.file_id is None:
            response = self.service.changes().watch(pageToken=self.page_token,
                                                    body={'id': self.channel_id,
                                                          'type': self.channel_type,
                                                          'address': self.channel_address}).execute()
        else:
            response = self.service.files().watch(fileId=self.file_id,
                                                  body={'id': self.channel_id,
                                                        'type': self.channel_type,
                                                        'address': self.channel_address}).execute()
        self.resource_id = response['resourceId']
        return self

    def stop(self):
        return self.service.channels().stop(body={'id': self.channel_id,
                                                  'resourceId': self.resource_id}).execute()
