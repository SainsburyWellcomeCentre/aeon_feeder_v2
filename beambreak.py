from neuroPico.port import AnalogPort
import time

def beambreak_calibration(beambreak:AnalogPort):
    MAX_VAL = 60000
    beambreak.setGain(1)
    for duty in range(2500, MAX_VAL, 100):
        beambreak.setPWM(duty)
        time.sleep_ms(50)
        if beambreak.value() > 50_000:
            break
    beambreak.setGain(MAX_VAL / beambreak.value())
