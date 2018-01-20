from .events import event_stream, Key, apply_deadzone


neutral = 'X1:     0  Y1:     0  X2:     0  Y2:     0  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0  '


def x_events(data_stream):
    return event_stream(data_stream)


class TestXEvents:
    def test_emit_on_A_pressed(self):
        output = [
            neutral,
            neutral.replace('A:0', 'A:1'),
        ]
        events = list(x_events(output))
        event = events[0]

        assert event.key == Key.A
        assert event.is_press()


    def test_emit_on_B_pressed(self):
        output = [
            neutral,
            neutral.replace('B:0', 'B:1'),
        ]
        events = list(x_events(output))
        event = events[0]

        assert event.key == Key.B
        assert event.is_press()


    def test_emits_X1(self):
        output = [
            neutral,
            neutral.replace('X1:     0', 'X1:  2272')
        ]

        events = list(x_events(output))
        event = events[0]

        assert event.key == Key.X1
        assert event.value == 0.0693359375


class TestDeadzone:
    def test_deadzone_sets_0(self):
        value = apply_deadzone(0.1, 0.2)
        assert value == 0

    def test_deadzone_scales_down(self):
        value = apply_deadzone(0.3, 0.1)
        assert 0 < value < 0.3
