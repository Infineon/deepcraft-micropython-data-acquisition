class Register:
    
    def __init__(
        self,
        device_address: int,
        bus
    )-> None:
        self._device_address = device_address
        self._bus = bus
        
    def _read_reg_into(self, reg, buf):
        self._bus.readfrom_mem_into(self._device_address, reg, buf)
            
    def _read_reg(self, reg_addr: int, read_length: int):
        buf = memoryview(self._bus.readfrom_mem(self._device_address, reg_addr, read_length))
        if read_length == 1:
            return int(buf[0])
        return buf
    
    def _write_reg(self, reg_addr: int, value):
        value = bytes([value])
        self._bus.writeto_mem(self._device_address, reg_addr, value)
