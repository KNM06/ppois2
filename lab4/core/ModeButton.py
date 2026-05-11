from core.Motor import Motor
from core.ControlButton import ControlButton


class ModeButton(ControlButton):
    def __init__(self, motor: Motor) -> None:
        super().__init__("Кнопка управления мощностью")
        self.motor: Motor = motor

    def press(self, level: int) -> None:
        self.motor.power_level = level
