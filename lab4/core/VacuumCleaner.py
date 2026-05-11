import json
import os
from core.Motor import Motor
from core.DustContainer import DustContainer
from core.Filter import Filter
from core.Attachment import Attachment
from core.PowerButton import PowerButton
from core.ModeButton import ModeButton
from core.Room import Room
from core.exceptions import (
    MotorStateError,
    ContainerFullException,
    FilterDegradedException,
)


class VacuumCleaner:
    def __init__(self) -> None:
        self._motor: Motor = Motor()
        self._container: DustContainer = DustContainer()
        self._filter: Filter = Filter()
        self._attachments: list[Attachment] = [
            Attachment("Стандартная щетка"),
            Attachment("Узкая насадка"),
        ]
        self._current_attachment: Attachment = self._attachments[0]
        self._power_button: PowerButton = PowerButton(self._motor)
        self._mode_button: ModeButton = ModeButton(self._motor)

    @property
    def motor(self) -> Motor:
        return self._motor

    @property
    def container(self) -> DustContainer:
        return self._container

    @property
    def filter(self) -> Filter:
        return self._filter

    @property
    def attachments(self) -> list[Attachment]:
        return self._attachments

    @property
    def current_attachment(self) -> Attachment:
        return self._current_attachment

    @property
    def power_button(self) -> PowerButton:
        return self._power_button

    @property
    def mode_button(self) -> ModeButton:
        return self._mode_button

    def change_attachment(self, index: int) -> None:
        if 0 <= index < len(self._attachments):
            self._current_attachment = self._attachments[index]
        else:
            raise ValueError("Неверный индекс насадки.")

    def add_attachment(self, name: str) -> None:
        self._attachments.append(Attachment(name))

    def remove_attachment(self, index: int) -> None:
        if 0 <= index < len(self._attachments):
            if len(self._attachments) == 1:
                raise ValueError("Невозможно удалить единственную насадку.")
            removed = self._attachments.pop(index)
            if self._current_attachment == removed:
                self._current_attachment = self._attachments[0]
        else:
            raise ValueError("Неверный индекс насадки.")

    def clean_room(self, room: Room) -> int:
        if not self._motor.is_on:
            raise MotorStateError("Пылесос выключен. Включите его для уборки.")

        if self._container.is_full():
            raise ContainerFullException(
                "Невозможно начать уборку: контейнер заполнен."
            )

        if self._filter.needs_replacement():
            raise FilterDegradedException(
                "Невозможно начать уборку: требуется замена фильтра."
            )

        if room.dust_amount == 0:
            return 0

        available_capacity = self._container.capacity - self._container.current_fill
        cleaning_power = self._motor.power_level * 35

        dust_to_collect = min(room.dust_amount, available_capacity, cleaning_power)

        self._container.add_dust(dust_to_collect)
        room.dust_amount -= dust_to_collect
        self._filter.degrade(dust_to_collect // 5)

        return dust_to_collect

    def empty_container(self) -> None:
        self._container.clean()

    def replace_filter(self) -> None:
        self._filter.replace()

    def maintenance(self) -> None:
        self.empty_container()
        self.replace_filter()
        if self._motor.is_on:
            self._motor.turn_off()

    def to_dict(self) -> dict:
        return {
            "motor": self._motor.to_dict(),
            "container": self._container.to_dict(),
            "filter": self._filter.to_dict(),
            "attachments": [a.to_dict() for a in self._attachments],
            "current_attachment_index": self._attachments.index(
                self._current_attachment
            )
            if self._current_attachment in self._attachments
            else 0,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VacuumCleaner":
        vacuum = cls()
        vacuum._motor = Motor.from_dict(data.get("motor", {}))
        vacuum._power_button = PowerButton(vacuum._motor)
        vacuum._mode_button = ModeButton(vacuum._motor)
        vacuum._container = DustContainer.from_dict(data.get("container", {}))
        vacuum._filter = Filter.from_dict(data.get("filter", {}))

        attachments_data = data.get("attachments", [])
        if attachments_data:
            vacuum._attachments = [Attachment.from_dict(a) for a in attachments_data]
            vacuum._current_attachment = vacuum._attachments[0]

        current_index = data.get("current_attachment_index", 0)
        if 0 <= current_index < len(vacuum._attachments):
            vacuum._current_attachment = vacuum._attachments[current_index]

        return vacuum

    def save_state(self, filename: str = "vacuum_state.json") -> None:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка при сохранении состояния: {e}")

    @classmethod
    def load_state(cls, filename: str = "vacuum_state.json") -> "VacuumCleaner":
        if not os.path.exists(filename):
            return cls()

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls.from_dict(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при загрузке состояния: {e}. Создан новый пылесос.")
            return cls()
