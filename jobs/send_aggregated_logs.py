import config
from chilli_pi.models import SensorData
from chilli_pi.google_logger import SpreadsheetLogger

sensor_data = SensorData(config.db['file'])
log_data = list(
    sensor_data.get_aggregated_values(config.log_aggregation_minutes)
)

light_switch_state = sensor_data.get_last_light_switch_state()
log_data.append(light_switch_state)

SpreadsheetLogger(
    config.google['credentials_path'],
    config.google['spreadsheet_id']
).log(log_data)
