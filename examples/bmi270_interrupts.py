import sensors.bmi270 as b
import time
from machine import I2C, Pin

i2c = I2C(scl='P0_2', sda='P0_3') # Correct I2C pins for PSOC6 AI Kit
data_rdy = False

def cback(event):
    global data_rdy
    data_rdy = True
    
def main(sensor):
    global data_rdy
    
    sensor.init()
    sensor.configure_data_ready_interrupt()
    accel_buf, gyro_buf = sensor.get_buffer()
    while True:
        if data_rdy:
            accx, accy, accz, gyrox, gyroy, gyroz = sensor.read_samples(accel_buf, gyro_buf)
            print(f"x:{accx:.2f}m/s2, y:{accy:.2f}m/s2, z{accz:.2f}m/s2")
            print("x:{:.2f}°/s, y:{:.2f}°/s, z{:.2f}°/s".format(gyrox, gyroy, gyroz))
            data_rdy = False

int_pin = Pin("P1_5", mode=Pin.IN, pull = Pin.PULL_DOWN)
int_pin.irq(handler=cback, trigger=Pin.IRQ_FALLING)

if __name__ == "__main__":
    config = {
        "bus": i2c,
        "accel_range": b.ACCEL_RANGE_2G,
        "gyro_range": b.GYRO_RANGE_250,
        "buffer_size": 6,
        "interrupt_config": int_pin
    }

    sensor = b.BMI270(config=config)
    main(sensor)

