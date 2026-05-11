import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.Filter import Filter
from core.exceptions import FilterDegradedException


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.filter = Filter()

    def test_initial_state(self):
        self.assertEqual(self.filter.wear_level, 0)

    def test_degrade(self):
        self.filter.degrade(10)
        self.assertEqual(self.filter.wear_level, 10)

    def test_degrade_limit(self):
        with self.assertRaises(FilterDegradedException):
            self.filter.degrade(101)
        self.assertEqual(self.filter.wear_level, 100)

    def test_replace(self):
        self.filter.degrade(50)
        self.filter.replace()
        self.assertEqual(self.filter.wear_level, 0)

    def test_needs_replacement(self):
        self.assertFalse(self.filter.needs_replacement())
        try:
            self.filter.degrade(100)
        except FilterDegradedException:
            pass
        self.assertTrue(self.filter.needs_replacement())

    def test_to_dict(self):
        self.filter.degrade(15)
        self.assertEqual(self.filter.to_dict(), {"wear_level": 15})

    def test_from_dict(self):
        data = {"wear_level": 42}
        f = Filter.from_dict(data)
        self.assertEqual(f.wear_level, 42)
