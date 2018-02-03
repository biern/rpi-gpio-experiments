from enum import Enum
from collections import namedtuple
import logging
import subprocess
import re

from .utils import readlines_by


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



xpad_buttons_map = {
    '0': Key.A,
    '1': Key.B,
    '2': Key.X,
    '3': Key.Y,
}


xpad_axes_map = {
    '0': Key.X1,
    '1': Key.X2,
    '2': Key.LT,
    '3': Key.Y1,
    '4': Key.Y2,
    '5': Key.RT,
}


EventBase = namedtuple('EventBase', ['key', 'value', 'old_value'])


class Event(EventBase):
    def is_press(self):
        return self.value == 1 and self.old_value == 0


def apply_deadzone(value, deadzone):
    scale = 1
    if value < 0:
        return (scale * min(0, value + deadzone)) / (scale - deadzone)
    return (scale * max(0, value - deadzone)) / (scale - deadzone)


def event_stream(data_stream, deadzone=0):
    data_stream = iter(data_stream)

    prev_state = None

    for line in data_stream:
        state = normalize_axes(parse_state(line), deadzone)

        if not prev_state:
            prev_state = state
            continue

        for key, value in state.items():
            prev_value = prev_state[key]
            if value != prev_value:
                yield Event(key, value, prev_value)

        prev_state = state


def normalize_axes(state, deadzone):
    result = {}
    for key, value in state.items():
        if key in (Key.X1, Key.X2, Key.Y1, Key.Y2):
            normalized = value / STICK_MAX
            value = apply_deadzone(normalized, deadzone)
        result[key] = value

    return result


def parse_state(line):
    axes, buttons = line.split('Buttons:')
    _, axes = axes.split('Axes:')

    buttons_state = parse_buttons(buttons)
    axes_state = parse_axes(axes)

    return { **buttons_state, **axes_state }


def parse_axes(text):
    text_pairs = filter(bool, re.findall(r'\d+\:\s*-?\d+', text))
    pairs = [p.split(':') for p in text_pairs]
    return dict([
        (xpad_axes_map.get(key, key), int(value))
        for key, value in pairs
    ])


def parse_buttons(text):
    text_pairs = filter(bool, text.split(' '))
    pairs = [p.split(':') for p in text_pairs]
    return dict([
        (xpad_buttons_map.get(key, key), value == 'on')
        for key, value in pairs
    ])


def xpad_event_stream(**kwargs):
    logging.info('Running xpad')
    proc = subprocess.Popen(
        ['jstest', '--normal', '/dev/input/js0'],
        stdout=subprocess.PIPE,
    )
    pipe = proc.stdout

    def iterator():
        try:
            for line in readlines_by(pipe, b'\r'):
                line = line.decode('utf-8')
                if 'error' in line.lower():
                    raise ValueError(line)
                if not line:
                    continue
                if not line.startswith('Axes'):
                    continue
                yield line.strip()
        finally:
            logging.info('Terminating jstest')
            proc.kill()

    return event_stream(iterator(), **kwargs)


if __name__ == "__main__":
    xpad_event_stream(deadzone=3000)
