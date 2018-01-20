import RPi.GPIO as GPIO
import time


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(18, 100)
    pwm.start(5)

    def set_angle(angle):
        duty = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(duty)


    set_angle(0)
    time.sleep(1)

    # set_angle(180)
    # time.sleep(1)

    set_angle(180)
    time.sleep(3)

finally:
    GPIO.cleanup()
