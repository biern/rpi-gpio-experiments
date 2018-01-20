import RPi.GPIO as GPIO

from rx.concurrency import ThreadPoolScheduler

from xrx.stream import x_stream
from xrx.events import Event, Key, xboxdrv_event_stream


class ServoControls:
    def __init__(self, pwm_pin, frequency, start_angle=0):
        self.pwm_pin = pwm_pin
        self.frequency = frequency
        self.start_angle = start_angle

    def setup(self):
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, self.frequency)
        self.pwm.start(self._angle_duty(self.start_angle))

    def _angle_duty(self, angle):
        assert -90 <= angle <= 90
        angle += 90
        return angle / 10.0 + 2.5

    def set_angle(self, angle):
        self.pwm.ChangeDutyCycle(self._angle_duty(angle))


class DCControls:
    def __init__(self, pin_a, pin_b, pwm_pin, frequency=100):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pwm_pin = pwm_pin
        self.frequency = frequency
        self.direction = 0

    def setup(self):
        GPIO.setup(self.pin_a, GPIO.OUT)
        GPIO.setup(self.pin_b, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.power_pwm = GPIO.PWM(self.pwm_pin, self.frequency)
        self.power_pwm.start(0)

    def forward(self):
        self.direction = 1
        GPIO.output(self.pin_a, GPIO.HIGH)
        GPIO.output(self.pin_b, GPIO.LOW)

    def backward(self):
        self.direction = -1
        GPIO.output(self.pin_a, GPIO.LOW)
        GPIO.output(self.pin_b, GPIO.HIGH)

    def speed(self, speed):
        self.power_pwm.ChangeDutyCycle(speed * 100)

    def run(self, value):
        if value > 0 and self.direction != 1:
            self.forward()
        if value < 0 and self.direction != -1:
            self.backward()

        self.speed(abs(value))


class XboxServo:
    def __init__(self, axis, controls, interval=100, reverse=False):
        self.axis = axis
        self.controls = controls
        self.interval = interval
        self.reverse = reverse

    def bind(self, stream):
        stream.filter(lambda e: e.key == self.axis) \
              .sample(self.interval) \
              .subscribe(self.on_event)

    def on_event(self, event):
        angle = int(event.value * 90)
        if self.reverse:
            angle = -angle
        self.controls.set_angle(angle)


class XboxDC:
    def __init__(self, axis, controls, interval=100, reverse=False):
        self.axis = axis
        self.controls = controls
        self.interval = interval
        self.reverse = reverse

    def bind(self, stream):
        stream.filter(lambda e: e.key == self.axis) \
              .sample(self.interval) \
              .subscribe(self.on_event)

    def on_event(self, event):
        value = -1 * event.value if self.reverse else event.value
        self.controls.run(value)


try:
    GPIO.setmode(GPIO.BCM)

    servo = ServoControls(18, 100)
    servo.setup()

    main = DCControls(pin_a=13, pin_b=6, pwm_pin=5)
    main.setup()

    scheduler = ThreadPoolScheduler(2)
    stream = x_stream(xboxdrv_event_stream(deadzone=0.3)).\
        publish()

    xbox_servo = XboxServo(Key.X1, servo, reverse=False)
    xbox_servo.bind(stream)

    xbox_dc = XboxDC(Key.Y2, main, reverse=True)
    xbox_dc.bind(stream)

    stream.sample(1000).subscribe(print)
    stream.connect()
finally:
    GPIO.cleanup()
