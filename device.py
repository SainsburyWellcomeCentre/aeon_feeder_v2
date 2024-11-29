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
    R_DUMMY = const(35)
    R_PEL_SND = const(36)
    R_WHEEL_ENCO = const(90)

    def __init__(
        self,
        led,
        clock,
        motor: Motor,
        encoder: AS5600,
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
        self.encoder = encoder
        self.threshold = threshold
        registers = {
            HarpDevice.R_DEVICE_NAME: ReadWriteReg(HarpTypes.U8, tuple(b"Feeder V2")),
            HarpDevice.R_WHO_AM_I: ReadOnlyReg(HarpTypes.U16, (1600,)),
            HarpDevice.R_HW_VERSION_H: ReadOnlyReg(HarpTypes.U8, (2,)),
            HarpDevice.R_HW_VERSION_L: ReadOnlyReg(HarpTypes.U8, (0,)),
            HarpDevice.R_FW_VERSION_H: ReadOnlyReg(HarpTypes.U8, (1,)),
            HarpDevice.R_FW_VERSION_L: ReadOnlyReg(HarpTypes.U8, (0,)),
            self.R_PEL_SND: PelletSendReg(HarpTypes.U16),
            self.R_BBK_DET: ReadOnlyReg(HarpTypes.U8, (0,)),
            self.R_DUMMY: ReadWriteReg(HarpTypes.U16, (0,)),
            self.R_WHEEL_ENCO: WheelAngleReg(encoder),
        }
        self.registers.update(registers)

        self.readAngleEvent = PeriodicEvent(
            self.R_WHEEL_ENCO,
            self.registers[self.R_WHEEL_ENCO],
            self.clock,
            self.txMessages,
            10,
        )

        self.beambreakFlag = False

        self.beambreakEvent = LooseEvent(self.R_BBK_DET, self.registers[self.R_BBK_DET], self.clock, self.txMessages)

        self.events.append(self.readAngleEvent)
        self.events.append(self.beambreakEvent)

        self.tasks.append(self._beambreak_task())
        self.tasks.append(self._pellet_task())

        self.btn.callback = self.button_callback

    async def _beambreak_task(self):
        lastStatus = False
        reg = self.registers[self.R_BBK_DET]
        while True:
            val = self.beambreak.value()
            isTriggerd = val > self.threshold
            self.beambreakFlag = isTriggerd
            if isTriggerd:
                self.motor.setSpeed(0)

            if lastStatus != isTriggerd:
                val = 255 if isTriggerd else 0
                reg.value = (val,)
                self.beambreakEvent.callback()
                await uasyncio.sleep(0.05)

            lastStatus = isTriggerd

            await uasyncio.sleep(0.001)

    async def _pellet_task(self):
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
        maxSpeed = 30000
        scale = 3000
        minSpeed = 6000
        speed = maxSpeed
        while True:

            if self.beambreakFlag:
                self.motor.setSpeed(0)
                break
            else:
                self.motor.setSpeed(speed)

            if speed > minSpeed:
                speed -= scale
            else:
                speed = maxSpeed

            await uasyncio.sleep(0.01)
