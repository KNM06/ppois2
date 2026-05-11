from core.exceptions import ContainerFullException


class DustContainer:
    def __init__(self, capacity: int = 100) -> None:
        self._capacity: int = capacity
        self._current_fill: int = 0

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def current_fill(self) -> int:
        return self._current_fill

    def add_dust(self, amount: int) -> None:
        if self._current_fill + amount > self._capacity:
            self._current_fill = self._capacity
            raise ContainerFullException("Контейнер для пыли заполнен.")
        self._current_fill += amount

    def clean(self) -> None:
        self._current_fill = 0

    def is_full(self) -> bool:
        return self._current_fill >= self._capacity

    def to_dict(self) -> dict:
        return {"capacity": self._capacity, "current_fill": self._current_fill}

    @classmethod
    def from_dict(cls, data: dict) -> "DustContainer":
        container = cls(data.get("capacity", 100))
        container._current_fill = data.get("current_fill", 0)
        return container
