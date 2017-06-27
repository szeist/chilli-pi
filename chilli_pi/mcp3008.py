import spidev


class MCP3008:
    def __init__(self, bus, device):
        self._spi = spidev.SpiDev()
        self._bus = bus
        self._device = device

    def read_volts(self, channel):
        adc_value = self._read_spi(channel)
        return self.convert_volts(adc_value)

    def _read_spi(self, channel):
        self._spi.open(self._bus, self._device)
        adc = self._spi.xfer2([1, (8 + channel) << 4, 0])
        self._spi.close()
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    @staticmethod
    def convert_volts(data):
        volts = (data * 3.3) / float(1023)
        volts = round(volts, 4)
        return volts



