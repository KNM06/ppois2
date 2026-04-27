import pygame
import os
from .Button import Button
from .InputBox import InputBox


class UIManager:
    """Менеджер для создания и хранения всех элементов интерфейса."""

    def __init__(self, screen_w, screen_h):
        self.help_text_lines = self._load_help_text()
        self.scroll_y = 0
        self.max_scroll = 0 
        self.build(screen_w, screen_h)

    def _load_help_text(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        filepath = os.path.join(base_dir, "assets", "rules.txt")

        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.readlines()
        return ["Файл правил (assets/rules.txt) не найден."]

    def build(self, screen_w, screen_h, old_text=""):
        btn_w = int(screen_w * 0.4)
        btn_h = int(screen_h * 0.08)
        start_x = (screen_w - btn_w) // 2
        font_s = int(btn_h * 0.45)

        step_y = int(screen_h * 0.10)
        start_y = int(screen_h * 0.30)

        self.btn_start = Button(
            start_x, start_y, btn_w, btn_h, "Локальная игра", font_size=font_s
        )
        self.btn_online = Button(
            start_x, start_y + step_y, btn_w, btn_h, "Онлайн игра", font_size=font_s
        )
        self.btn_records = Button(
            start_x,
            start_y + step_y * 2,
            btn_w,
            btn_h,
            "Таблица рекордов",
            font_size=font_s,
        )
        self.btn_help = Button(
            start_x, start_y + step_y * 3, btn_w, btn_h, "Справка", font_size=font_s
        )
        self.btn_exit = Button(
            start_x, start_y + step_y * 4, btn_w, btn_h, "Выход", font_size=font_s
        )

        self.menu_buttons = [
            self.btn_start,
            self.btn_online,
            self.btn_records,
            self.btn_help,
            self.btn_exit,
        ]
        self.btn_back = Button(
            20,
            20,
            int(screen_w * 0.15),
            int(screen_h * 0.06),
            "Назад",
            font_size=int(font_s * 0.8),
        )

        # --- ВОССТАНОВЛЕННЫЙ КОД МОДАЛЬНОГО ОКНА ---
        modal_w = btn_w + 100
        modal_h = int(screen_h * 0.45)
        self.modal_rect = pygame.Rect(0, 0, modal_w, modal_h)
        self.modal_rect.center = (screen_w // 2, screen_h // 2)

        input_y = self.modal_rect.y + int(modal_h * 0.45)
        btn_y = self.modal_rect.bottom - btn_h - 20

        self.input_box = InputBox(
            start_x, input_y, btn_w, int(screen_h * 0.06), text=old_text
        )
        self.btn_save = Button(
            start_x, btn_y, btn_w, btn_h, "Сохранить победу", font_size=font_s
        )
        self.btn_to_menu = Button(
            start_x, btn_y, btn_w, btn_h, "В главное меню", font_size=font_s
        )

    def draw_help_screen(self, screen, screen_w, screen_h):
        min_dim = min(screen_w, screen_h)
        font_size = max(int(min_dim * 0.035), 14)
        font_text = pygame.font.SysFont("Arial", font_size)

        clip_y = int(screen_h * 0.12)
        screen.set_clip(pygame.Rect(0, clip_y, screen_w, screen_h - clip_y))

        # === ИСПРАВЛЕНИЕ БАГА: Блокируем скролл ДО отрисовки текста ===
        if self.scroll_y < self.max_scroll:
            self.scroll_y = self.max_scroll

        y_offset = clip_y + 20 + self.scroll_y
        x_offset = int(screen_w * 0.1)
        max_width = screen_w - (x_offset * 2)

        for paragraph in self.help_text_lines:
            paragraph = paragraph.strip("\n")
            if not paragraph:
                y_offset += font_text.get_linesize()
                continue

            words = paragraph.split(" ")
            current_line = []

            for word in words:
                test_line = " ".join(current_line + [word])
                if font_text.size(test_line)[0] < max_width:
                    current_line.append(word)
                else:
                    text_surface = font_text.render(
                        " ".join(current_line), True, (220, 200, 180)
                    )
                    screen.blit(text_surface, (x_offset, y_offset))
                    y_offset += font_text.get_linesize() + 4
                    current_line = [word]

            if current_line:
                text_surface = font_text.render(
                    " ".join(current_line), True, (220, 200, 180)
                )
                screen.blit(text_surface, (x_offset, y_offset))
                y_offset += font_text.get_linesize() + 4

        # === Вычисляем max_scroll для следующего кадра ===
        content_height = y_offset - (clip_y + 20 + self.scroll_y)
        self.max_scroll = min(0, (screen_h - clip_y) - content_height - 50)

        if content_height < (screen_h - clip_y):
            self.max_scroll = 0
            self.scroll_y = 0

        screen.set_clip(None)
