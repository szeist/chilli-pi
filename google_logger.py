from __future__ import print_function

import os
from time import strftime
import httplib2
from apiclient import discovery
from apiclient.http import MediaIoBaseUpload
from oauth2client import client
from oauth2client.file import Storage
from dotenv import load_dotenv


class GoogleLogger:
    def __init__(self, credential_path):
        self._credentials = self._load_credentials(credential_path)

    def _get_api(self, api, version):
        http = self._credentials.authorize(httplib2.Http())
        return discovery.build(
            api,
            version,
            http=http
        )

    @staticmethod
    def _load_credentials(raw_credenttial_path):
        credential_path = os.path.expanduser(raw_credenttial_path)
        store = Storage(credential_path)
        return store.get()


class SpreadsheetLogger(GoogleLogger):
    _FIELDS = [
        'date',
        'light_full',
        'light_infrared',
        'light_visible',
        'light_lux',
        'pressure',
        'temperature',
        'humidity']

    def __init__(self, credential_path, spreadsheetId):
        GoogleLogger.__init__(self, credential_path)
        self._spreadsheetId = spreadsheetId

    def log(self, log_time, light_data, environmental_data):
        row = self._create_row(log_time, light_data, environmental_data)
        self._send_log([row])

    def _send_log(self, data):
        sheets_api = self._get_api('sheets', 'v4')

        return sheets_api.spreadsheets().values().append(
            spreadsheetId=self._spreadsheetId,
            range=self._get_spreadsheet_range(),
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': data}
        ).execute()

    def _get_spreadsheet_range(self):
        return 'A:' + chr(ord('A') + len(self._FIELDS))

    @staticmethod
    def _create_row(log_time, light_data, environmental_data):
        return [
            strftime('%Y-%m-%d %H:%M:%S', log_time),
            light_data['full'],
            light_data['infra'],
            light_data['visible'],
            light_data['lux'],
            environmental_data.pressure,
            environmental_data.temperature,
            environmental_data.humidity
        ]


class DriveLogger(GoogleLogger):
    def __init__(self, credential_path, folder_id):
        GoogleLogger.__init__(self, credential_path)
        self._folder_id = folder_id

    def logJpg(self, log_time, data):
        file_metadata = {
            'name': strftime('%Y%m%d%H%M%S.jpg', log_time),
            'parents': [self._folder_id]
        }

        drive_service = self._get_api('drive', 'v3')

        media = MediaIoBaseUpload(data, mimetype='image/jpeg', resumable=True)

        drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
