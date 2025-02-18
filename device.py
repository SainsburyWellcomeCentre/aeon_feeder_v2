from micropython import const
import uasyncio

from microharp.device import HarpDevice
from microharp.type import HarpTypes
from microharp.register import ReadWriteReg, ReadOnlyReg
from microharp.event import PeriodicEvent, LooseEvent

from neuroPico.motor import Motor
from neuroPico.driver.as5600 import AS5600
from neuroPico.port import AnalogPort
from neuroPico.utilty.debounce import DebouncedInput

from register import PelletSendReg


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
        super().__init__(led, clock, monitor=monitor, txqlen=100)
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
            self.R_WHEEL_ENCO: ReadOnlyReg(HarpTypes.U16, (0, 0)),
        }
        self.registers.update(registers)

        self.readAngleEvent = PeriodicEvent(
            self.R_WHEEL_ENCO,
            self.registers[self.R_WHEEL_ENCO],
            self.clock,
            self.txMessages,
            10,
        )

        self.beambreakEvent = LooseEvent(self.R_BBK_DET, self.registers[self.R_BBK_DET], self.clock, self.txMessages)

        self.events.append(self.readAngleEvent)
        self.events.append(self.beambreakEvent)

        self.tasks.append(self._encoder_task())
        self.tasks.append(self._pellet_task())

        self.btn.callback = self.button_callback

        self.beambreakDuty = self.beambreak.duty
        self.beambreak.setPWM(0)

    def button_callback(self, pin=-1):
        reg = self.registers[self.R_PEL_SND]
        reg.value = (1,)

    async def _encoder_task(self):
        reg = self.registers[self.R_WHEEL_ENCO]
        while True:
            reg.value = (
                self.encoder.read_angle_raw() << 2,
                self.encoder.read_mag() << 2,
            )
            await uasyncio.sleep(0)

    async def _pellet_task(self):
        reg = self.registers[self.R_PEL_SND]
        while True:
            val = reg.read(reg.typ)
            isTrigger = val[0] > 0

            if isTrigger:
                if await self.deliver_operation():
                    await self.beambreak_callback(255)
                    await self.wheel_check()
                    await self.beambreak_callback(0)
                reg.value = (0,)
            else:
                await uasyncio.sleep(0.002)

    async def wheel_check(self):
        reg = self.registers[self.R_WHEEL_ENCO]
        init_pos = reg.value[0]
        max_val = 16383
        threshold = 410  # 65535 in angle / 40 slot
        diff = 0
        while diff < threshold:
            pos = reg.value[0]
            diff = (pos - init_pos) if (pos >= init_pos) else (max_val - init_pos + pos)
            await uasyncio.sleep(0.02)

    async def beambreak_callback(self, val):
        reg = self.registers[self.R_BBK_DET]
        reg.value = (val,)
        self.beambreakEvent.callback()

    async def deliver_operation(self):
        maxSpeed = 28000
        scale = 50
        minSpeed = 28000
        speed = maxSpeed
        timeout = 0
        self.beambreak.setPWM(self.beambreakDuty)
        await uasyncio.sleep(0.001)
        while timeout < 65535:
            if self.beambreak.value() > self.threshold:
                while self.beambreak.value() > self.threshold:
                    self.motor.setSpeed(6000)
                    await uasyncio.sleep(0.001)
                self.beambreak.setPWM(0)
                self.motor.setSpeed(10000)
                await uasyncio.sleep(0.1)
                self.motor.setSpeed(0)
                return True
            else:
                self.motor.setSpeed(speed)

            if speed > minSpeed:
                speed -= scale
            else:
                speed = maxSpeed
                timeout += 1

            await uasyncio.sleep(0.001)
        return False
