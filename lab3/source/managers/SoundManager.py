import pygame
import os


class SoundManager:
    """Менеджер для управления звуковыми эффектами и фоновой музыкой."""

    def __init__(self):
        # инициализация микшера
        pygame.mixer.init()
        # путь к папке со звуками
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.sound_dir = os.path.join(base_dir, "assets", "sounds")

        # загрузка звуковых эффектов
        self.move_sound = self._load_sound("move.wav")
        self.capture_sound = self._load_sound("capture.wav")
        self.checkmate_sound = self._load_sound("checkmate.wav")
        self.current_music = None

    # безопасная загрузка звука
    def _load_sound(self, filename):
        """Безопасная загрузка звука (возвращает None, если файла нет или он битый)."""
        filepath = os.path.join(self.sound_dir, filename)
        if os.path.exists(filepath):
            try:
                return pygame.mixer.Sound(filepath)
            except pygame.error as e:
                print(f"Внимание: Не удалось загрузить звук '{filename}'. Ошибка: {e}")
                return None
        return None

    # проигрывает звук хода
    def play_move(self):
        if self.move_sound:
            self.move_sound.play()

    # проигрывает звук взятия фигуры
    def play_capture(self):
        if self.capture_sound:
            self.capture_sound.play()

    # включает фоновую музыку
    def play_music(self, filename):
        """Включает фоновую музыку, переключая треки."""
        # если музыка уже играет, ничего не делаем
        if self.current_music == filename:
            return

        filepath = os.path.join(self.sound_dir, filename)
        if os.path.exists(filepath):
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)  # -1 для зацикливания
                self.current_music = filename
            except pygame.error as e:
                print(
                    f"Внимание: Не удалось загрузить музыку '{filename}'. Ошибка: {e}"
                )

    # проигрывает звук мата
    def play_checkmate(self):
        if self.checkmate_sound:
            self.checkmate_sound.play()
