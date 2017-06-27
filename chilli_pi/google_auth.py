import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleAuth:
    _APPLICATION_NAME = 'Chilli Pi'
    _SCOPES = ('https://www.googleapis.com/auth/spreadsheets'
               ' https://www.googleapis.com/auth/drive.file')

    def __init__(self, client_secret_file, credential_file):
        self._client_secret_file = client_secret_file
        self._credential_path = os.path.abspath(credential_file)
        self._credential_store = Storage(self._credential_path)

    def check_credentials(self):
        credentials = self.get_credentials()
        return credentials and not credentials.invalid

    def get_credentials(self):
        return self._credential_store.get()

    def store_credentials(self):
        self._create_credentials_dir()
        flags = self._read_cmdline_flags()
        flags.noauth_local_webserver = True
        self._create_credentials(flags)

    def _create_credentials_dir(self):
        credential_dir = os.path.dirname(self._credential_path)
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

    def _create_credentials(self, flags):
        flow = client.flow_from_clientsecrets(
            self._client_secret_file,
            self._SCOPES)
        flow.user_agent = self._APPLICATION_NAME
        tools.run_flow(flow, self._credential_store, flags)

    @staticmethod
    def _read_cmdline_flags():
        import argparse
        return argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
