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

    R_BBK_DET = const(32)
    R_PEL_SND = const(36)
    R_WHEEL_ANG = const(90)
    R_DUMMY = const(35)

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
            self.R_PEL_SND: PelletSendReg(HarpTypes.U16),
            self.R_DUMMY: ReadWriteReg(HarpTypes.U16, (0,)),
            self.R_BBK_DET: ReadOnlyReg(HarpTypes.U8, (0,)),
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
        reg = self.registers[self.R_PEL_SND]
        while True:
            val = reg.read(reg.typ)
            isTrigger = val[0] > 0

            if isTrigger:
                await self.deliver_operation()
                reg.value = (0,)
            else:
                await uasyncio.sleep(0.002)

    def button_callback(self, pin=-1):
        reg = self.registers[self.R_PEL_SND]
        reg.value = (1,)

    async def deliver_operation(self):
        reg = self.registers[self.R_BBK_DET]
        speed = 50000
        while True:
            self.motor.setSpeed(speed)

            print(self.beambreak.value(), end="\t")
            print(speed, end="\t")
            print(self.threshold, end="\t\n")
            isDetected = self.beambreak.value() > self.threshold
            if isDetected:
                self.motor.setSpeed(0)
                break

            if speed > 9000:
                speed = round(0.9 * speed)
            else:
                speed = 9000
            await uasyncio.sleep(0.002)

        reg.value = (255,)
        self.beambreakEvent.callback()
        await uasyncio.sleep(0.01)
        reg.value = (0,)
        self.beambreakEvent.callback()
