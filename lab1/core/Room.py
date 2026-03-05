import random


class Room:
    def __init__(self, name: str, initial_dust: int = 0) -> None:
        self._name: str = name
        self._dust_amount: int = initial_dust

    @property
    def name(self) -> str:
        return self._name

    @property
    def dust_amount(self) -> int:
        return self._dust_amount

    @dust_amount.setter
    def dust_amount(self, value: int) -> None:
        if value < 0:
            self._dust_amount = 0
        else:
            self._dust_amount = value

    def accumulate_dust(self) -> None:
        self.dust_amount += random.randint(1, 5)

    def to_dict(self) -> dict:
        return {"name": self._name, "dust_amount": self.dust_amount}

    @classmethod
    def from_dict(cls, data: dict) -> "Room":
        return cls(data.get("name", "Unknown"), data.get("dust_amount", 0))
