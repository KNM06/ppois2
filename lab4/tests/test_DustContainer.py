import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.DustContainer import DustContainer
from core.exceptions import ContainerFullException


class TestDustContainer(unittest.TestCase):
    def setUp(self):
        self.container = DustContainer(capacity=10)

    def test_initial_state(self):
        self.assertEqual(self.container.current_fill, 0)
        self.assertEqual(self.container.capacity, 10)

    def test_add_dust(self):
        self.container.add_dust(5)
        self.assertEqual(self.container.current_fill, 5)

    def test_add_dust_full(self):
        self.container.add_dust(5)
        with self.assertRaises(ContainerFullException):
            self.container.add_dust(6)
        self.assertEqual(self.container.current_fill, 10)

    def test_clean(self):
        self.container.add_dust(5)
        self.container.clean()
        self.assertEqual(self.container.current_fill, 0)

    def test_is_full(self):
        self.assertFalse(self.container.is_full())
        self.container.add_dust(10)
        self.assertTrue(self.container.is_full())

    def test_to_dict(self):
        self.container.add_dust(3)
        self.assertEqual(self.container.to_dict(), {"capacity": 10, "current_fill": 3})

    def test_from_dict(self):
        data = {"capacity": 50, "current_fill": 20}
        container = DustContainer.from_dict(data)
        self.assertEqual(container.capacity, 50)
        self.assertEqual(container.current_fill, 20)
