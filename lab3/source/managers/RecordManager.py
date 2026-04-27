import json
import os


class RecordManager:
    """Менеджер для сохранения и загрузки Таблицы лидеров (Топ по победам)."""

    def __init__(self, filename="leaderboard.json"):
        # определяем путь к файлу рекордов
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.filepath = os.path.join(base_dir, "data", filename)
        self.records = self._load_records()

    # загружает рекорды из файла
    def _load_records(self):
        """Читает записи из файла."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    # добавляет победу игроку
    def add_win(self, name):
        """Добавляет +1 к победам игрока."""
        name = name.strip()
        if not name:
            name = "Аноним"

        # если игрока нет, создаем запись
        if name not in self.records:
            self.records[name] = {"wins": 0}

        # увеличиваем счетчик побед
        self.records[name]["wins"] += 1
        self._save_records()

    # сохраняет рекорды в файл
    def _save_records(self):
        """Записывает словарь в JSON файл."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    # получает список лучших игроков
    def get_top_players(self, limit=10):
        """Возвращает отсортированный список топ-игроков: [(Имя, Победы), ...]"""
        # превращаем словарь в список
        players = [(name, data["wins"]) for name, data in self.records.items()]
        # сортируем по победам
        players.sort(key=lambda x: x[1], reverse=True)
        return players[:limit]
