# sensors/pdm_pcm_sensor.py

from .sensor_interface import SensorInterface
import machine

class PDM_PCM(SensorInterface):
    def __init__(self, config=None):
        super().__init__(config)
        from machine import PDM_PCM
        self.PDM_PCM = PDM_PCM
        self.clk_pin = config.get("clk_pin", "P10_4")
        self.data_pin = config.get("data_pin", "P10_5")
        self.sample_rate = config.get("sample_rate", 16000)
        self.gain = config.get("gain", 20)
        self.buffer_size = config.get("buffer_size", 512)
        self.pdm = None

    def init(self):
        machine.freq(machine.AUDIO_PDM_24_576_000_HZ)
        self.pdm = self.PDM_PCM(
            0,
            sck=self.clk_pin,
            data=self.data_pin,
            sample_rate=self.sample_rate,
            decimation_rate=64,
            bits=self.PDM_PCM.BITS_16,
            format=self.PDM_PCM.MONO_LEFT,
            left_gain=self.gain,
            right_gain=self.gain,
        )
        self.pdm.init()

    def get_buffer(self):
        import array
        return array.array('h', [0] * self.buffer_size)

    def read_samples(self, buf):
        return self.pdm.readinto(buf)

    def get_format(self):
        return '<', 'h'

    def deinit(self):
        self.pdm.deinit()

