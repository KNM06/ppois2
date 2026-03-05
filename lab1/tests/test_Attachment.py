import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.Attachment import Attachment


class TestAttachment(unittest.TestCase):
    def test_init(self):
        att = Attachment("Test Nozzle")
        self.assertEqual(att.name, "Test Nozzle")

    def test_to_dict(self):
        att = Attachment("Nozzle")
        self.assertEqual(att.to_dict(), {"name": "Nozzle"})

    def test_from_dict(self):
        data = {"name": "Brush"}
        att = Attachment.from_dict(data)
        self.assertEqual(att.name, "Brush")
