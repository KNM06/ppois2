from core.Motor import Motor
from core.ControlButton import ControlButton


class PowerButton(ControlButton):
    def __init__(self, motor: Motor) -> None:
        super().__init__("Кнопка включения")
        self.motor: Motor = motor

    def press(self) -> None:
        if self.motor.is_on:
            self.motor.turn_off()
        else:
            self.motor.turn_on()
