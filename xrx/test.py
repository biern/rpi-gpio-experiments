from .events import event_stream, Key, apply_deadzone, event_stream


neutral = 'Axes:  0:     0  1:     0  2:     0  3:     0  4:     0  5:     0  6:     0  7:     0 Buttons:  0:off  1:off  2:off  3:off  4:off  5:off  6:off  7:off  8:off  9:off  10:off  11:off  12:off '


def x_events(data_stream):
    return event_stream(data_stream)


class TestXEvents:
    def test_emit_on_A_pressed(self):
        output = [
            neutral,
            neutral.replace(' 0:off', ' 0:on'),
        ]
        events = list(x_events(output))

        assert len(events) == 1

        event = events[0]
        assert event.key == Key.A
        assert event.is_press()


    def test_emit_on_B_pressed(self):
        output = [
            neutral,
            neutral.replace(' 1:off', ' 1:on'),
        ]
        events = list(x_events(output))

        assert len(events) == 1

        event = events[0]
        assert event.key == Key.B
        assert event.is_press()


    def test_emits_X1(self):
        output = [
            neutral,
            neutral.replace('0:     0', '0:  2272')
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
