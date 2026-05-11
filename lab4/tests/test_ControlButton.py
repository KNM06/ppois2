import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.ControlButton import ControlButton


class TestControlButton(unittest.TestCase):
    def test_press(self):
        b = ControlButton("B")
        self.assertEqual(b.name, "B")
        with self.assertRaises(NotImplementedError):
            b.press()
