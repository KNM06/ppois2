import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.Motor import Motor
from core.exceptions import MotorStateError


class TestMotor(unittest.TestCase):
    def test_all(self):
        m = Motor()
        self.assertFalse(m.is_on)
        m.turn_on()
        self.assertTrue(m.is_on)
        with self.assertRaises(MotorStateError):
            m.turn_on()
        m.turn_off()
        with self.assertRaises(MotorStateError):
            m.turn_off()

        m.power_level = 2
        self.assertEqual(m.power_level, 2)
        for v in [0, 4]:
            with self.assertRaises(ValueError):
                m.power_level = v
        self.assertEqual(Motor.from_dict(m.to_dict()).power_level, 2)
