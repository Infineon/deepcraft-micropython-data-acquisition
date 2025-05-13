# sensor_interface.py
class SensorInterface:
    def __init__(self, config=None):
        self.config = config or {}
        
    def init(self):
        raise NotImplementedError

    def get_buffer(self):
        raise NotImplementedError

    def read_samples(self, buf):
        raise NotImplementedError

    def get_format(self):
        raise NotImplementedError

    def deinit(self):
        raise NotImplementedError


