from neuroPico.port import AnalogPort
import time


def beambreak_calibration(beambreak: AnalogPort):

    MAX_DUTY = 57500
    MIN_DUTY = 27000
    pwm = 0
    beambreak.setGain(1)
    beambreak.setPWM(0)
    for duty in range(MIN_DUTY, MAX_DUTY, 250):
        beambreak.setPWM(duty)
        time.sleep_ms(1)
        if beambreak.value() > MIN_DUTY:
            pwm = duty
            break
    gain = MAX_DUTY / beambreak_avg(beambreak)
    beambreak.setGain(gain)

    threshold = round(beambreak_avg(beambreak) * 1.04)

    return threshold, gain, pwm


def beambreak_avg(beambreak: AnalogPort):
    sumVal = 0
    length = 50
    for _ in range(length):
        sumVal += beambreak.value()
        time.sleep_ms(1)
    return round(sumVal / length)
