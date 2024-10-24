from machine import Pin, SoftI2C
import uasyncio
from device import MyDevice
from neuroPico.neuropico import NeuroPico



theDevice = MyDevice(led_G, tof)
uasyncio.run(theDevice.main())
