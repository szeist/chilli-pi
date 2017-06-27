from time import strptime, strftime
import RPi.GPIO as GPIO
import config
from chilli_pi.models import SensorData


def is_light_time():
    start_time = strptime(config.light['start_time'], '%H:%M')
    end_time = strptime(config.light['end_time'], '%H:%M')

    current_time_str = strftime('%H:%M')
    current_time = strptime(current_time_str, '%H:%M')

    return current_time >= start_time and current_time <= end_time


def switch_light(state):
    if state:
        GPIO.output(config.board['light_switch_pin'], GPIO.LOW)
    else:
        GPIO.output(config.board['light_switch_pin'], GPIO.HIGH)


sensor_data = SensorData(config.db['file'])
light_value = sensor_data.get_current_avg_lux(
    timeframe_minutes=config.log_aggregation_minutes
) or 0

need_light = is_light_time() and light_value < config.light['switch_treshold']

switch_light(need_light)
