import unittest
import sys
import os
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.PowerButton import PowerButton


class TestPowerButton(unittest.TestCase):
    def test_press(self):
        m = MagicMock()
        b = PowerButton(m)
        m.is_on = False
        b.press()
        m.turn_on.assert_called()
        m.is_on = True
        b.press()
        m.turn_off.assert_called()
