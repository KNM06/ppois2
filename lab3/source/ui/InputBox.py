import pygame


class InputBox:
    """Класс для создания поля ввода текста."""

    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)

        # --- НОВЫЕ ЦВЕТА ---
        self.color_inactive = (180, 140, 100)  # Цвет светлого дерева
        self.color_active = (255, 215, 0)  # Золотой
        self.bg_color = (45, 30, 20)  # Темно-кофейный фон
        self.color = self.color_inactive

        self.text = text
        self.font = pygame.font.SysFont("Arial", int(h * 0.6))
        self.txt_surface = self.font.render(text, True, (255, 255, 255))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active = self.rect.collidepoint(event.pos)
                self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 12:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, screen):
        # Рисуем сплошной фон
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        # Рисуем рамку
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        # Рисуем текст
        screen.blit(
            self.txt_surface,
            (
                self.rect.x + 10,
                self.rect.y
                + self.rect.height // 2
                - self.txt_surface.get_height() // 2,
            ),
        )
