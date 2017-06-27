import os
from time import strftime
import httplib2
from apiclient import discovery
from apiclient.http import MediaIoBaseUpload
from oauth2client.file import Storage


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
    def __init__(self, credential_path, spreadsheetId):
        GoogleLogger.__init__(self, credential_path)
        self._spreadsheetId = spreadsheetId

    def log(self, data):
        sheets_api = self._get_api('sheets', 'v4')

        return sheets_api.spreadsheets().values().append(
            spreadsheetId=self._spreadsheetId,
            range=self._get_spreadsheet_range(data),
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': [data]}
        ).execute()

    @staticmethod
    def _get_spreadsheet_range(data):
        return 'A:' + chr(ord('A') + len(data))


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
