import json
import os
from core.VacuumCleaner import VacuumCleaner
from core.Room import Room
from core.exceptions import VacuumException


def load_rooms(filename: str = "rooms_state.json") -> list[Room]:
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Room.from_dict(r) for r in data]
        except (json.JSONDecodeError, IOError):
            pass
    return [Room("Гостиная", 40), Room("Спальня", 15), Room("Кухня", 150)]


def save_rooms(rooms: list[Room], filename: str = "rooms_state.json") -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rooms], f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка при сохранении комнат: {e}")


def main() -> None:
    vacuum = VacuumCleaner.load_state()
    rooms = load_rooms()

    while True:
        print("\n--- Меню пылесоса ---")
        status = "ВКЛ" if vacuum.motor.is_on else "ВЫКЛ"
        print(
            f"[{status}] Мощность: {vacuum.motor.power_level} | Насадка: {vacuum.current_attachment.name}"
        )
        print(
            f"Контейнер: {vacuum.container.current_fill}/{vacuum.container.capacity} | Износ фильтра: {vacuum.filter.wear_level}%"
        )
        print("-" * 25)
        print("1. Нажать кнопку включения")
        print("2. Уборка помещения")
        print("3. Очистить контейнер")
        print("4. Заменить фильтры")
        print("5. Техническое обслуживание")
        print("6. Сменить насадку")
        print("7. Нажать кнопку управления мощностью")
        print("8. Добавить новое помещение")
        print("9. Удалить помещение")
        print("10. Добавить насадку")
        print("11. Удалить насадку")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                vacuum.power_button.press()
                print("Состояние питания изменено.")
            elif choice == "2":
                if not rooms:
                    print("Сперва добавьте хотя бы одно помещение.")
                else:
                    print("\nДоступные помещения:")
                    for i, room in enumerate(rooms):
                        print(
                            f"{i}. {room.name} (Уровень загрязненности: {room.dust_amount})"
                        )

                    room_idx = int(input("Выберите номер помещения для уборки: "))
                    if 0 <= room_idx < len(rooms):
                        target_room = rooms[room_idx]
                        collected = vacuum.clean_room(target_room)
                        if collected > 0:
                            print(f"Уборка проведена. Собрано {collected} ед. пыли.")
                            print(
                                f"Осталось пыли в помещении: {target_room.dust_amount}"
                            )
                        else:
                            print("Помещение уже чистое!")
                    else:
                        print("Неверный номер помещения.")
            elif choice == "3":
                vacuum.empty_container()
                print("Контейнер очищен.")
            elif choice == "4":
                vacuum.replace_filter()
                print("Фильтр заменен.")
            elif choice == "5":
                vacuum.maintenance()
                print("Техническое обслуживание выполнено.")
            elif choice == "6":
                print("\nДоступные насадки:")
                for i, att in enumerate(vacuum.attachments):
                    print(f"{i}. {att.name}")
                idx = int(input("Выберите номер насадки: "))
                vacuum.change_attachment(idx)
                print(f"Насадка изменена на {vacuum.current_attachment.name}")
            elif choice == "7":
                level = int(input("Введите требуемый уровень мощности (1-3): "))
                vacuum.mode_button.press(level)
                print(f"Установлен режим мощности: {level}")
            elif choice == "8":
                new_name = input("Введите название нового помещения: ")
                initial_dust = int(input("Введите начальный уровень загрязненности: "))
                rooms.append(Room(new_name, initial_dust))
                print(f"Помещение '{new_name}' успешно добавлено.")
            elif choice == "9":
                if not rooms:
                    print("Нет помещений для удаления.")
                else:
                    print("\nДоступные помещения:")
                    for i, room in enumerate(rooms):
                        print(f"{i}. {room.name}")
                    del_idx = int(input("Выберите номер помещения для удаления: "))
                    if 0 <= del_idx < len(rooms):
                        removed = rooms.pop(del_idx)
                        print(f"Помещение '{removed.name}' удалено.")
                    else:
                        print("Неверный номер помещения.")
            elif choice == "10":
                new_att_name = input("Введите название новой насадки: ")
                if new_att_name.strip():
                    vacuum.add_attachment(new_att_name)
                    print(f"Насадка '{new_att_name}' успешно добавлена.")
                else:
                    print("Название насадки не может быть пустым.")
            elif choice == "11":
                print("\nДоступные насадки:")
                for i, att in enumerate(vacuum.attachments):
                    print(f"{i}. {att.name}")
                del_idx = int(input("Выберите номер насадки для удаления: "))
                vacuum.remove_attachment(del_idx)
                print("Насадка удалена.")
            elif choice == "0":
                vacuum.save_state()
                save_rooms(rooms)
                print("Состояние пылесоса и комнат сохранено.")
                break
            else:
                print("Неверный выбор.")

            for room in rooms:
                room.accumulate_dust()

        except VacuumException as e:
            print(f"Ошибка пылесоса: {e}")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()
