import uasyncio
from device import MyDevice
from neuroPico.neuropico import NeuroPico
from neuroPico.driver.as5600 import AS5600
from neuroPico.port import Port
from calibration import beambreak_calibration

myController = NeuroPico()

myled = myController.LED
myled.setColour((0, 30, 0))

myMotor = myController.MOTOR
myMotor.setVoltage(24)
myMotor.setFrequency(25_000)
myMotor.enable()

myController.CLK_nEN.value(0)
myCLK = myController.CLK_IN

mySensor = AS5600(myController.I2C)

myBeambreak = myController.PORT1
myBeambreak.mode = Port.ANG
threshold, _, _ = beambreak_calibration(myBeambreak)


myBTN = myController.BTNB


theDevice = MyDevice(myled, myCLK, myMotor, mySensor, myBeambreak, myBTN, threshold)
uasyncio.run(theDevice.main())
