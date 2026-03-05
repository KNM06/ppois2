from core.exceptions import MotorStateError


class Motor:
    def __init__(self) -> None:
        self._is_on: bool = False
        self._power_level: int = 1

    @property
    def is_on(self) -> bool:
        return self._is_on

    @property
    def power_level(self) -> int:
        return self._power_level

    @power_level.setter
    def power_level(self, level: int) -> None:
        if not (1 <= level <= 3):
            raise ValueError("Уровень мощности должен быть от 1 до 3.")
        self._power_level = level

    def turn_on(self) -> None:
        if self._is_on:
            raise MotorStateError("Мотор уже включен.")
        self._is_on = True

    def turn_off(self) -> None:
        if not self._is_on:
            raise MotorStateError("Мотор уже выключен.")
        self._is_on = False

    def to_dict(self) -> dict:
        return {"is_on": self._is_on, "power_level": self._power_level}

    @classmethod
    def from_dict(cls, data: dict) -> "Motor":
        motor = cls()
        motor._is_on = data.get("is_on", False)
        motor._power_level = data.get("power_level", 1)
        return motor
