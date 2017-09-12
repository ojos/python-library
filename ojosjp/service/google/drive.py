# -*- coding: utf-8 -*-
from .oauth import Certification

class Drive(Certification):
    SERVICE_NAME = 'drive'
    SERVICE_VERSION = 'v3'
    SERVICE_SCOPES = {'drive': 'https://www.googleapis.com/auth/drive',
                      'drive.appdata': 'https://www.googleapis.com/auth/drive.appdata',
                      'drive.file': 'https://www.googleapis.com/auth/drive.file',
                      'drive.metadata': 'https://www.googleapis.com/auth/drive.metadata',
                      'drive.metadata.readonly': 'https://www.googleapis.com/auth/drive.metadata.readonly',
                      'drive.photos.readonly': 'https://www.googleapis.com/auth/drive.photos.readonly',
                      'drive.readonly': 'https://www.googleapis.com/auth/drive.readonly',
                      'drive.scripts': 'https://www.googleapis.com/auth/drive.scripts'}

    @property
    def scopes(self):
        logger.info('START scopes')
        if self._scopes is None:
            self._scopes = [self.SERVICE_SCOPES['drive']]
        logger.info('RETURN %s', self._scopes)
        logger.info('END scopes')
        return self._scopes
