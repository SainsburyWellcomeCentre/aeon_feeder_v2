from neuroPico.port import AnalogPort
import time


def beambreak_calibration(beambreak: AnalogPort):
    MAX_DUTY = 50000
    MIN_DUTY = 10000

    gain = 1
    while gain < 3:
        beambreak.setPWM(MIN_DUTY)
        gain = MAX_DUTY / beambreak_avg(beambreak) / 2
        time.sleep_ms(100)
    beambreak.setGain(gain)
    pwm = 0
    for duty in range(MIN_DUTY, MAX_DUTY, 100):
        beambreak.setPWM(duty)
        time.sleep_ms(10)
        if beambreak.value() > MAX_DUTY:
            pwm = duty
            break

    threshold = beambreak_avg(beambreak) + 4000

    return threshold, gain, pwm


def beambreak_avg(beambreak: AnalogPort):
    sumVal = 0
    length = 50
    for _ in range(length):
        sumVal += beambreak.value()
        time.sleep_ms(1)
    return round(sumVal / length)
