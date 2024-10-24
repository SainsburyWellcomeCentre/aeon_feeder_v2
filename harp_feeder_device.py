from micropython import const
import uasyncio
from microharp.device import HarpDevice
from microharp.type import HarpTypes
from microharp.register import ReadWriteReg, ReadOnlyReg, OperationalCtrlReg
from harp_tof_registers import RangeReg
import time
from microharp.event import PeriodicEvent


class MyDevice(HarpDevice):
    """My Harp device."""

    R_PEL_SND = const(33)
    R_PEL_COUNT = const(34)
    R_BBK_VAL = const(35)
    R_BBK_THLD = const(36)
    R_BBK_DET = const(37)
    R_BBK_GAIN = const(38)
    R_WHEEL_COUNT = const(39)
    R_WHEEL_ANG = const(40)
    R_WHEEL_THLD = const(41)
    R_AUTO_EN = const(42)

    def __init__(self, led, tof, monitor=None):
        """Constructor.

        Connects the logical device to its physical interfaces, creates the register map.
        """
        super().__init__(led, monitor=monitor)
        registers = {
            HarpDevice.R_DEVICE_NAME: ReadWriteReg(HarpTypes.U8, tuple(b"My Feeder")),
            HarpDevice.R_WHO_AM_I: ReadOnlyReg(HarpTypes.U16, (1233,)),
            # HarpDevice.R_HW_VERSION_H: ReadOnlyReg(HarpTypes.U8, (1,)),
            # HarpDevice.R_HW_VERSION_L: ReadOnlyReg(HarpTypes.U8, (0,)),
            # HarpDevice.R_FW_VERSION_H: ReadOnlyReg(HarpTypes.U8, (1,)),
            # HarpDevice.R_FW_VERSION_L: ReadOnlyReg(HarpTypes.U8, (0,)),
            self.R_PEL_SND: RangeReg(tof),
            self.R_PEL_COUNT : RangeReg(tof),
            self.R_BBK_VAL : RangeReg(tof),
            self.R_BBK_THLD : RangeReg(tof),
            self.R_BBK_DET : RangeReg(tof),
            self.R_BBK_GAIN : RangeReg(tof),
            self.R_WHEEL_COUNT : RangeReg(tof),
            self.R_WHEEL_ANG : RangeReg(tof),
            self.R_WHEEL_THLD : RangeReg(tof),
            self.R_AUTO_EN : RangeReg(tof)
        }
        self.registers.update(registers)

        # self.readRangeEvent = PeriodicEvent(
        #     MyDevice.Range_VAL,
        #     self.registers[MyDevice.Range_VAL],
        #     self.sync,
        #     self.txMessages,
        #     30,
        # )

        # self.events.append(self.readRangeEvent)
