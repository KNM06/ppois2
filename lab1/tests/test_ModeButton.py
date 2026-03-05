import unittest
import sys
import os
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.ModeButton import ModeButton


class TestModeButton(unittest.TestCase):
    def test_press(self):
        m = MagicMock()
        ModeButton(m).press(2)
        self.assertEqual(m.power_level, 2)
