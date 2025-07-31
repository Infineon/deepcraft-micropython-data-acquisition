import struct

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
        
    def _write_burst(self, reg, data, chunk=16):
        for i in range(len(data) // chunk):
            self._write_reg(_BMI270_REG_INIT_ADDR0, 0x00)
            self._write_reg(_BMI270_REG_INIT_ADDR1, i)
            offs = i * chunk
            self._write_reg(reg, data[offs : offs + chunk])
            init_addr = ((i + 1) * chunk) // 2
            self._write_reg(_BMI270_REG_INIT_ADDR0, (init_addr & 0x0F))
            self._write_reg(_BMI270_REG_INIT_ADDR1, (init_addr >> 4) & 0xFF)
            
    def _read_reg(self, reg_addr: int, read_length: int):
        buf = memoryview(self._bus.readfrom_mem(self._device_address, reg_addr, read_length))
        if read_length == 1:
            return int(buf[0])
        return buf
    
    def _write_reg(self, reg_addr: int, value):
        #write_value = struct.pack(format, value)
        value = bytes([value])
        self._bus.writeto_mem(self._device_address, reg_addr, value)
