from micropython import const
import uasyncio

from microharp.device import HarpDevice
from microharp.type import HarpTypes
from microharp.register import HarpRegister, ReadWriteReg, ReadOnlyReg
from microharp.event import PeriodicEvent, LooseEvent

from neuroPico.motor import Motor
from neuroPico.driver.as5600 import AS5600
from neuroPico.port import AnalogPort
from neuroPico.utilty.debounce import DebouncedInput

from register import PelletSendReg, WheelAngleReg


class MyDevice(HarpDevice):
    """My Harp device."""

    R_PEL_SND = const(33)
    R_BBK_DET = const(37)
    R_BBK_RAW = const(44)
    R_WHEEL_ANG = const(90)

    def __init__(
        self,
        led,
        clock,
        motor: Motor,
        sensor: AS5600,
        beambreak: AnalogPort,
        btn: DebouncedInput,
        threshold,
        monitor=None,
    ):
        """Constructor.

        Connects the logical device to its physical interfaces, creates the register map.
        """
        super().__init__(led, clock, monitor=monitor)
        self.beambreak = beambreak
        self.motor = motor
        self.btn = btn
        self.sensor = sensor
        self.threshold = threshold
        registers = {
            HarpDevice.R_DEVICE_NAME: ReadWriteReg(HarpTypes.U8, tuple(b"Feeder V2")),
            HarpDevice.R_WHO_AM_I: ReadOnlyReg(HarpTypes.U16, (1600,)),
            HarpDevice.R_HW_VERSION_H: ReadOnlyReg(HarpTypes.U8, (2,)),
            HarpDevice.R_HW_VERSION_L: ReadOnlyReg(HarpTypes.U8, (0,)),
            HarpDevice.R_FW_VERSION_H: ReadOnlyReg(HarpTypes.U8, (1,)),
            HarpDevice.R_FW_VERSION_L: ReadOnlyReg(HarpTypes.U8, (0,)),
            self.R_PEL_SND: PelletSendReg(motor),
            self.R_BBK_DET: ReadOnlyReg(HarpTypes.U8, (1,)),
            self.R_BBK_RAW: ReadWriteReg(HarpTypes.U16, (0,)),
            self.R_WHEEL_ANG: WheelAngleReg(sensor),
        }
        self.registers.update(registers)

        self.readAngleEvent = PeriodicEvent(
            self.R_WHEEL_ANG,
            self.registers[self.R_WHEEL_ANG],
            self.clock,
            self.txMessages,
            10,
        )

        self.beambreakEvent = LooseEvent(self.R_BBK_DET, self.registers[self.R_BBK_DET], self.clock, self.txMessages)

        self.events.append(self.readAngleEvent)
        self.events.append(self.beambreakEvent)

        self.tasks.append(self._beambreak_task())

        self.btn.callback = self.button_callback

    async def _beambreak_task(self):
        reg = self.registers[self.R_BBK_RAW]
        while True:
            adc = self.beambreak.value()
            reg.write(reg.typ, (adc,))
            if adc < self.threshold:
                self.motor.setSpeed(0)
                self.beambreakEvent.callback()
                await uasyncio.sleep(0.1)
            await uasyncio.sleep(0.05)

    def button_callback(self, pin=-1):
        reg = self.registers[self.R_PEL_SND]
        reg.write(reg.typ, (1,))
