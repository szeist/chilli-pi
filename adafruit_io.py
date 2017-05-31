import logging
import json
from time import strftime
import requests


class Adafruit_IO():
    _API_BASE_URL = 'https://io.adafruit.com/api/v2'
    _API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, api_user, api_key):
        self._api_user = api_user
        self._api_key = api_key

    def send_data(self, feed, time, data):
        feed_data = {
            'value': data,
            'created_at': strftime(self._API_DATE_FORMAT, time)
        }

        response = requests.post(
            self._API_BASE_URL + '/%s/feeds/%s/data' % (self._api_user, feed),
            headers=self._get_request_headers(),
            data=json.dumps(feed_data)
        )

        self._log_result(response, feed, data)

        return response

    def _get_request_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-AIO-Key': self._api_key
        }

    @staticmethod
    def _log_result(response, feed, data):
        if response.status_code != 200:
            logging.error(
                'Adafruit_IO status=%d, response=%s, feed=%s, data=%s',
                response.status_code, response.text, feed, data
            )
