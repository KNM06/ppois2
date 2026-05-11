import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.VacuumCleaner import VacuumCleaner
from core.Room import Room
from core.exceptions import (
    MotorStateError,
    ContainerFullException,
    FilterDegradedException,
)


class TestVacuumCleaner(unittest.TestCase):
    TEST_FILE = "test_vac.json"

    def setUp(self):
        self.vc = VacuumCleaner()

    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_attachments(self):
        self.vc.add_attachment("N")
        self.vc.change_attachment(2)
        self.assertEqual(self.vc.current_attachment.name, "N")
        self.vc.remove_attachment(2)
        self.assertEqual(len(self.vc.attachments), 2)
        self.vc.change_attachment(1)
        self.vc.remove_attachment(1)
        self.assertEqual(self.vc.current_attachment.name, "Стандартная щетка")
        for i in [5, -1]:
            with self.assertRaises(ValueError):
                self.vc.change_attachment(i)
            with self.assertRaises(ValueError):
                self.vc.remove_attachment(i)
        with self.assertRaises(ValueError):
            self.vc.remove_attachment(0)

    def test_cleaning(self):
        r = Room("R", 100)
        with self.assertRaises(MotorStateError):
            self.vc.clean_room(r)
        self.vc.motor.turn_on()
        self.vc.clean_room(r)
        self.assertEqual(self.vc.container.current_fill, 35)
        self.assertEqual(self.vc.clean_room(Room("E", 0)), 0)

        self.vc.container._current_fill = 100
        with self.assertRaises(ContainerFullException):
            self.vc.clean_room(r)
        self.vc.container.clean()

        self.vc.filter._wear_level = 100
        with self.assertRaises(FilterDegradedException):
            self.vc.clean_room(r)

        self.vc.maintenance()
        self.assertEqual(self.vc.filter.wear_level, 0)
        self.assertFalse(self.vc.motor.is_on)

    def test_state(self):
        self.vc.mode_button.press(2)
        d = self.vc.to_dict()
        self.assertEqual(VacuumCleaner.from_dict(d).motor.power_level, 2)
        self.vc.save_state(self.TEST_FILE)
        self.assertEqual(VacuumCleaner.load_state(self.TEST_FILE).motor.power_level, 2)

        self.vc._current_attachment = "Unknown"
        self.assertEqual(self.vc.to_dict()["current_attachment_index"], 0)
        self.assertEqual(
            VacuumCleaner.from_dict(
                {"current_attachment_index": -1}
            ).current_attachment.name,
            "Стандартная щетка",
        )
