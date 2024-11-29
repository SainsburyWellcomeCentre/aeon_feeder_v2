from microharp.register import ReadWriteReg, ReadOnlyReg
from microharp.type import HarpTypes
from neuroPico.motor import Motor
from neuroPico.driver.as5600 import AS5600


class PelletSendReg(ReadWriteReg):
    """Read/write register with debug print."""

    def write(self, typ, value):
        self.value = (1,)


class WheelAngleReg(ReadOnlyReg):
    """Read/write register with debug print."""

    def __init__(self, snsr: AS5600):
        super().__init__(HarpTypes.U16, (0, 0))
        self._snsr = snsr

    def read(self, typ):
        self.value = (
            self._snsr.read_angle_raw() * 16,
            self._snsr.read_mag() * 16,
        )
        return super().read(typ)
