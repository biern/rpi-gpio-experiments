import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

Motor1A = 13
Motor1B = 6
Motor1P = 5

try:
    GPIO.setup(Motor1A, GPIO.OUT)
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1P, GPIO.OUT)

    power_pwm = GPIO.PWM(Motor1P, 100)
    power_pwm.start(0)

    print("Turning motor on")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)

    for i in range(5):
        power_pwm.ChangeDutyCycle(30 + i * 10)
        sleep(1)

    power_pwm.ChangeDutyCycle(100)
    sleep(1)

    # GPIO.output(Motor1A,GPIO.LOW)
    # GPIO.output(Motor1B,GPIO.HIGH)

    # sleep(2)
    # print "Stopping motor"
    # GPIO.output(Motor1E,GPIO.LOW)
finally:
    GPIO.cleanup()
