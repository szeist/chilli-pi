import RPi.GPIO as GPIO
import config

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(config.board['soil_moisture_switch_pin'], GPIO.OUT)
GPIO.setup(config.board['light_switch_pin'], GPIO.OUT)
