import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

log_aggregation_minutes = 5

board = {
    'soil_moisture_switch_pin': 23,
    'light_switch_pin': 24,
    'tsl2561_address': 0x39,
    'tsl2561_port': 1,
    'bme280_address': 0x76,
    'bme_280_port': 1,
    'ad_soil_moisture_channel': 0,
    'mcp3008_bus': 0,
    'mcp3008_device': 0,
}

db = {
    'file': 'chilli.db'
}

google = {
    'folder_id': os.getenv('GOOGLE_FOLDER_ID'),
    'spreadsheet_id': os.getenv('GOOGLE_SPREADSHEET_ID'),
    'credentials_path': os.getenv('GOOGLE_CREDENTIALS_PATH')
}

light = {
    'switch_treshold': 5000,  # 7500
    'start_time': '06:00',
    'end_time': '21:00',
}
