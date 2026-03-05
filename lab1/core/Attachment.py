class Attachment:
    def __init__(self, name: str) -> None:
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    def to_dict(self) -> dict:
        return {"name": self._name}

    @classmethod
    def from_dict(cls, data: dict) -> "Attachment":
        return cls(data.get("name", "Unknown"))
