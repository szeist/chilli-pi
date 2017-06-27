from __future__ import print_function
from chilli_pi.google_auth import GoogleAuth

CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIAL_FILE = '.credentials'

google_auth = GoogleAuth(CLIENT_SECRET_FILE, CREDENTIAL_FILE)
if google_auth.check_credentials():
    print('Credentials OK')
else:
    google_auth.store_credentials()
    print('Storing cretentials in %s' % CREDENTIAL_FILE)
