import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.ModeButton import ModeButton
from core.Motor import Motor


class TestModeButton(unittest.TestCase):
    def setUp(self):
        self.motor = Motor()
        self.button = ModeButton(self.motor)

    def test_press(self):
        self.button.press(2)
        self.assertEqual(self.motor.power_level, 2)
        self.button.press(3)
        self.assertEqual(self.motor.power_level, 3)

    def test_press_invalid(self):
        with self.assertRaises(ValueError):
            self.button.press(4)
