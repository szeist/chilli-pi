from __future__ import print_function

import os
from os.path import join, dirname
from time import gmtime
from io import BytesIO
import smbus2
import bme280
from picamera import PiCamera
from dotenv import load_dotenv

from adafruit_io import Adafruit_IO
from tsl2561 import TSL2561
from google_logger import SpreadsheetLogger, DriveLogger

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TSL2561_ADDRESS = 0x39
TSL2561_PORT = 1
BME280_ADDRESS = 0x77
BME_280_PORT = 1
AIO_KEY = os.getenv('AIO_KEY')
AIO_USER = os.getenv('AIO_USER')
LOG_FILE_BASE = os.getenv('HOME') + '/chilli'
GOOGLE_FOLDER_ID = os.getenv('GOOGLE_FOLDER_ID')
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')


def read_bme280():
    bus = smbus2.SMBus(BME_280_PORT)
    bme280.load_calibration_params(bus, BME280_ADDRESS)

    return bme280.sample(bus, BME280_ADDRESS)


def capture_image():
    camera = PiCamera()
    stream = BytesIO()
    camera.capture(stream, format='jpeg', resize=(720, 540))
    stream.seek(0)
    return stream


tsl2561 = TSL2561(0x39, 1)

light_data = tsl2561.read()
environmental_data = read_bme280()

log_time = gmtime()

SpreadsheetLogger(GOOGLE_CREDENTIALS_PATH, GOOGLE_SPREADSHEET_ID).log(
    log_time,
    light_data,
    environmental_data
)

image = capture_image()
DriveLogger(GOOGLE_CREDENTIALS_PATH, GOOGLE_FOLDER_ID).logJpg(
    gmtime(),
    image
)

aio = Adafruit_IO(AIO_USER, AIO_KEY)
aio.send_data('chilli-light-full', log_time, light_data['full'])
aio.send_data('chilli-light-infrared', log_time, light_data['infra'])
aio.send_data('chilli-light-visible', log_time, light_data['visible'])
aio.send_data('chilli-light-lux', log_time, light_data['lux'])
aio.send_data('chilli-pressure', log_time, environmental_data.pressure)
aio.send_data('chilli-temperature', log_time, environmental_data.temperature)
aio.send_data('chilli-humidity', log_time, environmental_data.humidity)
