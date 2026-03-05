import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.PowerButton import PowerButton
from core.Motor import Motor


class TestPowerButton(unittest.TestCase):
    def setUp(self):
        self.motor = Motor()
        self.button = PowerButton(self.motor)

    def test_press(self):
        self.button.press()
        self.assertTrue(self.motor.is_on)

        self.button.press()
        self.assertFalse(self.motor.is_on)
