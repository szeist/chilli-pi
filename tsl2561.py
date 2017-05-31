import time
import smbus


class TSL2561:
    _CONTROL_REGISTER = 0x00
    _TIMING_REGISTER = 0x01
    _COMMAND_REGISTER = 0x80
    _DATA0_REGISTER = 0x0C
    _DATA1_REGISTER = 0x0E

    _CONTROL_POWER_UP = 0x03
    _CONTROL_POWER_DOWN = 0x00

    _LOW_GAIN = 0x00
    _AUTO_INTEGRATION = 0x0
    _INTERATION_402MS = 0x02

    _INTEGRATION_NORMALIZATION = 402.0/402
    _GAIN_NORMALIZATION = 16  # For value 1X

    def __init__(self, address, port):
        self._i2c_addr = address
        self._i2c_port = port

        self._bus = smbus.SMBus(self._i2c_port)

    def read(self):
        self._power_on()
        self._config_ad_converter()

        time.sleep(0.5)

        data = self._read_register(self._DATA0_REGISTER)
        data1 = self._read_register(self._DATA1_REGISTER)

        self._power_off()

        d0 = self._regval_to_int(data)
        d1 = self._regval_to_int(data1)

        lux = self._calc_lux(d0, d1)

        return {
            'full': d0,
            'infra': d1,
            'visible': d0 - d1,
            'lux': lux
        }

    def _power_on(self):
        self._bus.write_byte_data(
            self._i2c_addr,
            self._CONTROL_REGISTER | self._COMMAND_REGISTER,
            self._CONTROL_POWER_UP
        )

    def _power_off(self):
        self._bus.write_byte_data(
            self._i2c_addr,
            self._CONTROL_REGISTER | self._COMMAND_REGISTER,
            self._CONTROL_POWER_DOWN
        )

    def _config_ad_converter(self):
        self._bus.write_byte_data(
            self._i2c_addr,
            self._TIMING_REGISTER | self._COMMAND_REGISTER,
            self._LOW_GAIN | self._AUTO_INTEGRATION | self._INTERATION_402MS
        )

    def _read_register(self, register):
        return self._bus.read_i2c_block_data(
            self._i2c_addr,
            register | self._COMMAND_REGISTER,
            2
        )

    def _calc_lux(self, d0, d1):
        if d0 == 0:
            return 0

        ratio = d1 / d0

        d0 *= self._INTEGRATION_NORMALIZATION
        d1 *= self._INTEGRATION_NORMALIZATION

        d0 *= self._GAIN_NORMALIZATION
        d1 *= self._GAIN_NORMALIZATION

        if ratio < 0.5:
            return 0.0304 * d0 - 0.062 * d0 * pow(ratio, 1.4)
        elif ratio < 0.61:
            return 0.0224 * d0 - 0.031 * d1
        elif ratio < 0.80:
            return 0.0128 * d0 - 0.0153 * d1
        elif ratio < 1.30:
            return 0.00146 * d0 - 0.00112 * d1
        else:
            return 0.0

    @staticmethod
    def _regval_to_int(data):
        return data[1] << 8 | data[0]
