# coding: utf-8

import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)

try:

    TRIG = 20

    ECHO = 21


    print "Distance Measurement In Progress"

    GPIO.setup(TRIG,GPIO.OUT)

    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)

    print "Waiting For Sensor To Settle"

    time.sleep(2)

    while True:
        measures = []
        for i in range(10):
            GPIO.output(TRIG, True)

            time.sleep(0.00001)

            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
              pulse_start = time.time()

            while GPIO.input(ECHO)==1:
              pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            measures.append(round(distance, 2))

        measures = sorted(measures)
        result = sum(measures[1:-1]) / (len(measures) - 2)
        print "Distance:", result ,"cm"

        time.sleep(1)

finally:
    GPIO.cleanup()
