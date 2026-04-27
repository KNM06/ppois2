import pygame


class Button:
    """класс для создания кнопок меню."""

    def __init__(self, x, y, width, height, text, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)

        # цвета кнопок
        self.base_color = (140, 90, 60)  # основной цвет
        self.hover_color = (170, 110, 80)  # цвет при наведении
        self.text_color = (255, 255, 255)  # цвет текста

        self.is_hovered = False

    # рисует кнопку
    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered else self.base_color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(
            center=self.rect.center
        )  # центрирование текста
        screen.blit(text_surface, text_rect)

    # проверяет, наведена ли мышь на кнопку
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    # проверяет, нажата ли кнопка
    def is_clicked(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # проверка нажатия левой кнопки мыши
            if self.is_hovered:
                return True
        return False
