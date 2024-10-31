from microharp.register import ReadWriteReg, ReadOnlyReg
from microharp.type import HarpTypes
from neuroPico.motor import Motor
from neuroPico.driver.as5600 import AS5600


class PelletSendReg(ReadWriteReg):
    """Read/write register with debug print."""

    def __init__(self, motor: Motor):
        super().__init__(HarpTypes.U8)
        self._motor = motor

    def read(self, typ):
        super().read(typ)
        return self.value

    def write(self, typ, value):
        super().write(typ, value)
        if value[0]:
            self._motor.setSpeed(6500)


class WheelAngleReg(ReadOnlyReg):
    """Read/write register with debug print."""

    def __init__(self, snsr: AS5600):
        super().__init__(HarpTypes.FLOAT)
        self._snsr = snsr

    def read(self, typ):
        self.value = (self._snsr.readAngle(),)
        return super().read(typ)
