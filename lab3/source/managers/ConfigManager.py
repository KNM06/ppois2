import json
import os

class ConfigManager:
    """Класс для управления настройками игры через JSON-файл."""
    
    def __init__(self, config_filename="config.json"):
        # Так как скрипт лежит в папке src, а конфиг в корне, нужно правильно указать путь
        # Поднимаемся на один уровень вверх от папки src
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_path = os.path.join(base_dir, 'data', config_filename)
        self.config_data = self._load_config()

    def _load_config(self):
        """Загружает данные из JSON файла."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Файл конфигурации не найден по пути: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as file:
            return json.load(file) # Превращаем JSON в словарь Python

    def get_window_settings(self):
        return self.config_data.get("window", {})

    def get_board_settings(self):
        return self.config_data.get("board", {})
        
    def get_network_settings(self):
        return self.config_data.get("network", {})

# Блок для проверки работоспособности файла (запустится только если запустить этот файл напрямую)
if __name__ == "__main__":
    try:
        config = ConfigManager()
        window_settings = config.get_window_settings()
        print("Конфигурация успешно загружена!")
        print(f"Разрешение экрана: {window_settings['width']}x{window_settings['height']}")
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")