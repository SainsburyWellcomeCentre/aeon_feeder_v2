from microharp.register import ReadOnlyReg
from microharp.type import HarpTypes


# class RangeReg(ReadOnlyReg):
#     """Read/write register with debug print."""

#     def __init__(self, tof: VL53LX):
#         super().__init__(HarpTypes.FLOAT)
#         self.tof = tof

#     def read(self, typ):
#         self.value = (self.tof.read_mm(),)
#         return super().read(typ)
