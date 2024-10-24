from machine import Pin, SoftI2C
import uasyncio
from harp_tof_device import MyDevice
from driver.vl53lx import VL53LX

led_G = Pin(22, Pin.OUT, value=1)
led_R = Pin(21, Pin.OUT, value=1)
led_B = Pin(25, Pin.OUT, value=1)

i2c = SoftI2C(scl=23, sda=24, freq=100000)
tof = VL53LX(i2c)

theDevice = MyDevice(led_G, tof)
uasyncio.run(theDevice.main())
