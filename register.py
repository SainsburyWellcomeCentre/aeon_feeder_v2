from microharp.register import ReadWriteReg


class PelletSendReg(ReadWriteReg):
    """Read/write register with debug print."""

    def write(self, typ, value):
        self.value = (1,)
