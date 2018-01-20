import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

pin = 18

try:
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin ,GPIO.HIGH)
    sleep(3)
finally:
    GPIO.cleanup()
