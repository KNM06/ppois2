class ControlButton:
    def __init__(self, name: str) -> None:
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    def press(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Метод press должен быть реализован в дочернем классе."
        )
