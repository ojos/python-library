# -*- coding: utf-8 -*-
from logging import getLogger

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ...decorator import retries

from .drive import Drive
from .exception import GoogleException

logger = getLogger(__name__)


class Spreadsheet(object):
    _worksheet = None
    _fields = None
    _key = None

    @property
    @retries()
    def records(self):
        logger.info('START records')
        records = self._worksheet.get_all_records()
        logger.info('SET records=%s', records)
        logger.info('END records')
        return records

    @retries()
    def __init__(self, credential_dict, file_id, title, scopes=[Drive.SERVICE_SCOPES['drive']]):
        logger.info('START __init__')
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential_dict,
                                                                       scopes=scopes)
        logger.info('SET credentials=%s', '{}'.format(credentials.__dict__))
        self._worksheet = gspread.authorize(credentials).open_by_key(file_id).worksheet(title)
        self._fields = list(filter(lambda s:s != '', self._worksheet.row_values(1)))
        self._key = self._fields[0]
        logger.info('SET self._worksheet=%s', '{}'.format(self._worksheet.__dict__))
        logger.info('SET self._fields=%s', self._fields)
        logger.info('SET self._key=%s', self._key)
        logger.info('END __init__')

    def get_by_key(self, key):
        logger.info('START get_by_key')
        is_include = False
        records = self.records
        logger.info('SET records=%s', records)
        row = 1
        for i in range(len(records)):
            row = i + 2
            if records[i][self._key] == key:
                is_include = True
                break

        if not is_include:
            row += 1

        cells = self._worksheet.range(row, 1, row, len(self._fields))
        logger.info('RETURN cells=%s, row=%s, is_include=%s', cells, row, is_include)
        logger.info('END get_by_key')
        return cells, row, is_include

    @retries()
    def insert(self, record, force=True):
        logger.info('START insert')
        cells, row, is_include = self.get_by_key(record[self._key])
        if is_include and not force:
            raise GoogleException()

        for key, value in record.items():
            i = self._fields.index(key)
            cells[i].value = value

        self._worksheet.update_cells(cells)
        logger.info('RETURN %s', cells)
        logger.info('END insert')
        return cells

    def to_dict(self, cells):
        return {self._fields[i]: cells[i].value for i in range(len(self._fields))}
