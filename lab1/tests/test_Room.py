import unittest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.Room import Room


class TestRoom(unittest.TestCase):
    def test_all(self):
        r = Room("A", 10)
        self.assertEqual(r.name, "A")
        r.dust_amount = -1
        self.assertEqual(r.dust_amount, 0)
        with patch("random.randint", return_value=5):
            r.accumulate_dust()
            self.assertEqual(r.dust_amount, 5)
        self.assertEqual(Room.from_dict(r.to_dict()).name, "A")
