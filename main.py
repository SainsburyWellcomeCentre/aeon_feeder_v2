import uasyncio
from device import MyDevice
from neuroPico.neuropico import NeuroPico
from neuroPico.driver.as5600 import AS5600
from neuroPico.port import Port
from micropython import const
from beambreak import beambreak_calibration

BBK_TH = const(54_500)


myController = NeuroPico()

myled = myController.LED
myled.setColour((0, 30, 0))

myMotor = myController.MOTOR
myMotor.setVoltage(24)
myMotor.enable()


myController.CLK_nEN.value(0)
myCLK = myController.CLK_IN

mySensor = AS5600(myController.I2C)

myBeambreak = myController.PORT1
myBeambreak.mode = Port.ANG
beambreak_calibration(myBeambreak)


myBTN = myController.BTNB


theDevice = MyDevice(myled, myCLK, myMotor, mySensor, myBeambreak, myBTN, BBK_TH)
uasyncio.run(theDevice.main())
