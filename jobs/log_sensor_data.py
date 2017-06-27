from time import sleep
import bme280
import smbus2
import RPi.GPIO as GPIO
import config
from chilli_pi.tsl2561 import TSL2561
from chilli_pi.mcp3008 import MCP3008
from chilli_pi.models import SensorData


def read_bme280():
    bus = smbus2.SMBus(config.board['bme_280_port'])
    bme280.load_calibration_params(bus, config.board['bme280_address'])
    return bme280.sample(bus, config.board['bme280_address'])


def read_soil_moisture():
    GPIO.output(config.board['soil_moisture_switch_pin'], GPIO.HIGH)
    sleep(2)
    value = mcp3008.read_volts(config.board['ad_soil_moisture_channel'])
    GPIO.output(config.board['soil_moisture_switch_pin'], GPIO.LOW)
    return value


def read_light_switch_state():
    return GPIO.input(config.board['soil_moisture_switch_pin']) != GPIO.HIGH


tsl2561 = TSL2561(
    config.board['tsl2561_address'],
    config.board['tsl2561_port']
)
mcp3008 = MCP3008(
    config.board['mcp3008_bus'],
    config.board['mcp3008_device']
)

light_data = tsl2561.read()
environmental_data = read_bme280()
soil_moisture = read_soil_moisture()
light_state = read_light_switch_state()

sensor_data = SensorData(config.db['file'])
sensor_data.add(
    light_infrared=light_data['infra'],
    light_visible=light_data['visible'],
    light_lux=light_data['lux'],
    pressure=environmental_data.pressure,
    temperature=environmental_data.temperature,
    humidity=environmental_data.humidity,
    soil_moisture=soil_moisture,
    light_switch_state=light_state
)
