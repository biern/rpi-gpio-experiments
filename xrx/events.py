from enum import Enum
from typing import NamedTuple
import logging
import subprocess
import re

s = re.compile('[ :]')
STICK_MAX = 32768


class Key(Enum):
    X1 = 'X1'
    Y1 = 'Y1'
    X2 = 'X2'
    Y2 = 'Y2'
    du = 'du'
    dd = 'dd'
    dl = 'dl'
    dr = 'dr'
    back = 'back'
    guide = 'guide'
    start = 'start'
    TL = 'TL'
    TR = 'TR'
    A = 'A'
    B = 'B'
    X = 'X'
    Y = 'Y'
    LB = 'LB'
    RB = 'RB'
    LT = 'LT'
    RT = 'RT'


class Event(NamedTuple):
    key: Key
    value: float
    old_value: float

    def is_press(self):
        return self.value == 1 and self.old_value == 0

    def __str__(self):
        return 'Event(%s,%d,%d)' % (self.key, self.value, self.old_value)


def apply_deadzone(value, deadzone):
    scale = 1
    if value < 0:
        return (scale * min(0, value + deadzone)) / (scale - deadzone)
    return (scale * max(0, value - deadzone)) / (scale - deadzone)


def event_stream(data_stream, deadzone=0):
    data_stream = iter(data_stream)

    def build_event_line(line):
        data = list(filter(bool, s.split(line[:-1])))
        return {data[x]: int(data[x+1]) for x in range(0, len(data), 2)}

    prev = build_event_line(next(data_stream))

    for line in data_stream:
        data = build_event_line(line)
        for key in data:
            if key in ('X1', 'X2', 'Y1', 'Y2'):
                normalized = data[key] / STICK_MAX
                data[key] = apply_deadzone(normalized, deadzone)
            if data[key] == prev[key]:
                continue
            event = Event(Key(key), data[key], prev[key])
            yield event

        prev = data


def xboxdrv_event_stream(**kwargs):
    logging.info('Running xboxdrv')
    proc = subprocess.Popen(
        ['xboxdrv', '--no-uinput', '--detach-kernel-driver'],
        stdout=subprocess.PIPE,
    )
    pipe = proc.stdout

    def iterator():
        try:
            while True:
                line = pipe.readline().decode('utf-8')
                if 'error' in line.lower():
                    raise ValueError(line)
                if not line:
                    continue
                if len(line) != 140:
                    continue
                yield line
        finally:
            logging.info('Terminating xboxdrv')
            proc.kill()

    return event_stream(iterator(), **kwargs)
