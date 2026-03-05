from core.exceptions import FilterDegradedException


class Filter:
    def __init__(self) -> None:
        self._wear_level: int = 0

    @property
    def wear_level(self) -> int:
        return self._wear_level

    def degrade(self, amount: int) -> None:
        self._wear_level += amount
        if self._wear_level >= 100:
            self._wear_level = 100
            raise FilterDegradedException("Фильтр изношен и требует замены.")

    def replace(self) -> None:
        self._wear_level = 0

    def needs_replacement(self) -> bool:
        return self._wear_level >= 100

    def to_dict(self) -> dict:
        return {"wear_level": self._wear_level}

    @classmethod
    def from_dict(cls, data: dict) -> "Filter":
        filter_obj = cls()
        filter_obj._wear_level = data.get("wear_level", 0)
        return filter_obj
