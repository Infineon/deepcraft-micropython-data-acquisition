# The `BMI270` class is a sensor interface for the BMI270 sensor that provides methods for
# initialization, setting ranges, reading acceleration and gyroscope data, and configuring interrupts.
from sensors.bmi270_config_file import bmi270_config_file
from sensors.sensor_interface import SensorInterface
from sensors import bmi270_i2c_helper as b
import time
from micropython import const
from machine import I2C
import array
import micropython
import sys

# Acceleration Range
ACCEL_RANGE_2G = const(0b00)
ACCEL_RANGE_4G = const(0b01)
ACCEL_RANGE_8G = const(0b10)
ACCEL_RANGE_16G = const(0b11)
acceleration_range_values = (
    ACCEL_RANGE_2G,
    ACCEL_RANGE_4G,
    ACCEL_RANGE_8G,
    ACCEL_RANGE_16G,
)

# Gyro range
GYRO_RANGE_2000 = const(0b000)
GYRO_RANGE_1000 = const(0b001)
GYRO_RANGE_500 = const(0b010)
GYRO_RANGE_250 = const(0b011)
GYRO_RANGE_125 = const(0b100)
gyro_range_values = (
    GYRO_RANGE_2000,
    GYRO_RANGE_1000,
    GYRO_RANGE_500,
    GYRO_RANGE_250,
    GYRO_RANGE_125,
)

# BMI270 Reg Stack
_BMI270_REG_CHIP_ID           =   const(0x00)
_BMI270_REG_ERR_REG           =   const(0x02)
_BMI270_REG_STATUS            =   const(0x03)
_BMI270_REG_DATA_0            =   const(0x04)
_BMI270_REG_DATA_1            =   const(0x05)
_BMI270_REG_DATA_2            =   const(0x06)
_BMI270_REG_DATA_3            =   const(0x07)
_BMI270_REG_DATA_4            =   const(0x08)
_BMI270_REG_DATA_5            =   const(0x09)
_BMI270_REG_DATA_6            =   const(0x0A)
_BMI270_REG_DATA_7            =   const(0x0B)
_BMI270_REG_DATA_8_ACC_X_LSB  =   const(0x0C)
_BMI270_REG_DATA_9_ACC_X_MSB  =   const(0x0D)
_BMI270_REG_DATA_10_ACC_Y_LSB =   const(0x0E)
_BMI270_REG_DATA_11_ACC_Y_MSB =   const(0x0F)
_BMI270_REG_DATA_12_ACC_Z_LSB =   const(0x10)
_BMI270_REG_DATA_13_ACC_Z_MSB =   const(0x11)
_BMI270_REG_DATA_14_GYR_X_LSB =   const(0x12)
_BMI270_REG_DATA_15_GYR_X_MSB =   const(0x13)
_BMI270_REG_DATA_16_GYR_Y_LSB =   const(0x14)
_BMI270_REG_DATA_17_GYR_Y_MSB =   const(0x15)
_BMI270_REG_DATA_18_GYR_Z_LSB =   const(0x16)
_BMI270_REG_DATA_19_GYR_Z_MSB =   const(0x17)
_BMI270_REG_INTERNAL_STATUS   =   const(0x21)
_BMI270_REG_ACC_CONF          =   const(0x40) 
_BMI270_REG_ACC_RANGE         =   const(0x41)
_BMI270_REG_GYRO_CONF         =   const(0x42)
_BMI270_REG_GYRO_RANGE        =   const(0x43)
_BMI270_REG_INT1_IO_CTRL      =   const(0x53)
_BMI270_REG_INT2_IO_CTRL      =   const(0x54)
_BMI270_REG_INT_LATCH         =   const(0x55)
_BMI270_REG_INT1_MAP_FEAT     =   const(0x56)
_BMI270_REG_INT2_MAP_FEAT     =   const(0x57)
_BMI270_REG_INT_MAP_DATA      =   const(0x58)
_BMI270_REG_INIT_CTRL         =   const(0x59)
_BMI270_REG_INIT_ADDR0        =   const(0x5B)
_BMI270_REG_INIT_ADDR1        =   const(0x5C)
_BMI270_REG_INIT_DATA         =   const(0x5E)
_BMI270_REG_PWR_CONF          =   const(0x7C)
_BMI270_REG_PWR_CTRL          =   const(0x7D)
_BMI270_REG_CMD               =   const(0x7E)

ACCEL_SCALE = (2, 4, 8, 16)
GYRO_SCALE = (2000, 1000, 500, 250, 125)

class BMI270(SensorInterface):
    def __init__(self, config=None):
        super().__init__(config)

        if config is None or "bus" not in config:
            raise ValueError("An I2C bus should be initialized by user")

        self._bus = config["bus"]
        self._address = config.get("address", 0x68)
        self._acceleration_range = config.get("acceleration_range", ACCEL_RANGE_2G)
        self._gyro_range = config.get("gyro_range", GYRO_RANGE_250)
        self._accel_scale = config.get("accel_scale", 4)
        self._gyro_scale = config.get("gyro_scale", 2000)
        self.reg = b.Register(self._address, self._bus) # Create an object of Register class to allow reg read and write
        self._int_config = config.get("interrupt_config", None)
        self.scratch = memoryview(array.array("h", [0, 0, 0])) #For direct accel and gyro API call
        
    def get_device_id(self): 
        """Get device id of BMI270 sensor.
        """
        return self.reg._read_reg(_BMI270_REG_CHIP_ID, 1)

    def get_internal_status(self):
        """Get the status of the sensor.
        """
        return self.reg._read_reg(_BMI270_REG_INTERNAL_STATUS, 1)
    
    def set_normal_power_mode(self):
        """Sets the sensor to operate in normal power mode.
        """
        self.reg._write_reg(_BMI270_REG_PWR_CTRL, 0x0E)
        time.sleep(0.1)
        self.reg._write_reg(_BMI270_REG_ACC_CONF, 0xA8)
        time.sleep(0.1)
        self.reg._write_reg(_BMI270_REG_GYRO_CONF, 0xA9)
        time.sleep(0.1)
        self.reg._write_reg(_BMI270_REG_PWR_CONF, 0x02)
        time.sleep(0.1)
        
    def set_accel_range(self, accel_scale):
        """Set the range for acceleration. Possible values are : 2, 4, 8, 16.
        """
        self.accel_scale = 32768/accel_scale
        self.reg._write_reg(_BMI270_REG_ACC_RANGE, ACCEL_SCALE.index(accel_scale))
        
    def set_gyro_range(self, gyro_scale):
        """Set the range for gyro. Possible values are: 2000, 1000, 500, 250, 125.
        """
        self.gyro_scale = 32768/gyro_scale
        self.reg._write_reg(_BMI270_REG_GYRO_RANGE, GYRO_SCALE.index(gyro_scale))
            
    def load_config_file(self) -> None:
        """Load the configuration file mandatory for BMI270 sensor to initialize.
        """
        if self.get_internal_status() == 0x01:
            print(hex(self._address), " --> Initialization already done")
        else:
            from sensors.bmi270_config_file import bmi270_config_file

            print(hex(self._address), " --> Initializing...")
            self.reg._write_reg(_BMI270_REG_PWR_CONF, 0x00)
            time.sleep_us(450)
            self.reg._write_reg(_BMI270_REG_INIT_CTRL, 0x00)
            for i in range(256):
                self.reg._write_reg(_BMI270_REG_INIT_ADDR0, 0x00)
                self.reg._write_reg(_BMI270_REG_INIT_ADDR1, i)
                time.sleep(0.03)
                self._bus.writeto_mem(
                    self._address,
                    0x5E,
                    bytes(bmi270_config_file[i * 32 : (i + 1) * 32]),
                )
                time.sleep(0.000020)
            self.reg._write_reg(_BMI270_REG_INIT_CTRL, 0x01)
            time.sleep(0.02)
            print(
                hex(self._address),
                " --> Initialization status: "
                + "{:08b}".format(self.get_internal_status())
                + "\t(00000001 --> OK)",
            )
        
    def init(self):
        """ Initializes the sensor by loading configuration file, setting power mode and acceleration and gyro ranges.
        """
        self.load_config_file()
        self.set_normal_power_mode()
        self.set_accel_range(self._accel_scale)
        self.set_gyro_range(self._gyro_scale)
    
    @micropython.native
    def acceleration(self):
        """Public API to get directly acceleration values in m/s^2.
        """
        f = self.accel_scale
        self.reg._read_reg_into(_BMI270_REG_DATA_8_ACC_X_LSB, self.scratch)
        return (self.scratch[0] / f, self.scratch[1] / f, self.scratch[2] / f)
    
    @micropython.native
    def gyro(self):
        """Public API to get directly gyro values in degrees/sec.
        """
        f = self.gyro_scale
        self.reg._read_reg_into(_BMI270_REG_DATA_14_GYR_X_LSB, self.scratch)
        return (self.scratch[0] / f, self.scratch[1] / f, self.scratch[2] / f)
        
    
    def configure_data_ready_interrupt(self):
        """Configure data ready interrupt for INT1 channel.
        """
        if self._int_config is not None:
            self.reg._write_reg(_BMI270_REG_INT_MAP_DATA, 0x04)
            self.reg._write_reg(_BMI270_REG_INT1_IO_CTRL, 0x08)
            self.reg._write_reg(_BMI270_REG_INT_LATCH, 0x00)
        else:
            raise ValueError("Interrupt on pin must be configured")
        
    def get_buffer(self):
        """ Creates buffers to hold acceleration and gyroscope values and returns.
        """
        scratch_accel = memoryview(array.array("h", [0, 0, 0]))
        scratch_gyro = memoryview(array.array("h", [0, 0, 0]))
        return scratch_accel, scratch_gyro
    
    @micropython.native
    def read_samples(self, scratch_accel, scratch_gyro):
        """ Fills scratch_accel and scratch_gyro buffers with acceleration and gyro values and returns normalized values.
        """
        f1 = self.accel_scale
        f2 = self.gyro_scale
        self.reg._read_reg_into(_BMI270_REG_DATA_8_ACC_X_LSB, scratch_accel)
        self.reg._read_reg_into(_BMI270_REG_DATA_14_GYR_X_LSB, scratch_gyro)
        return (scratch_accel[0] / f1, scratch_accel[1] / f1, scratch_accel[2] / f1, scratch_gyro[0] / f2, scratch_gyro[1] / f2, scratch_gyro[2] / f2)

    def get_format(self):
        """ Returns format and endianess to hold data in buffer.
        """
        return '<', 'h'

    def deinit(self):
        """ Deinitializes sensor module. 
        """
        self._bus.deinit()
        self._int_config.deinit()

