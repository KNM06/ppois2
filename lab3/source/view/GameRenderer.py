import pygame
import os
import math


class GameRenderer:
    def __init__(self, screen, config_manager):
        self.screen = screen
        self.config_manager = config_manager

        # получение цветов из конфига
        board_settings = config_manager.get_board_settings()
        self.light_color = tuple(board_settings["light_color"])
        self.dark_color = tuple(board_settings["dark_color"])

        # названия колонок и рядов
        self.files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]

        self.images = {}

        # состояние анимации фигур
        self.anim_piece = None
        self.anim_start_pos = None
        self.anim_end_pos = None
        self.anim_current_frame = 0
        self.anim_total_frames = 20  # длительность анимации в кадрах
        self.is_animating = False
        self.dying_info = None  # информация об исчезающей фигуре

        # пересчет размеров элементов
        self.update_dimensions()

    # обновляет размеры элементов при изменении окна
    def update_dimensions(self):
        """вычисляет размеры элементов на основе размера окна."""
        screen_w, screen_h = self.screen.get_size()
        min_dim = min(screen_w, screen_h)

        # место для координат по краям
        self.margin = max(int(min_dim * 0.08), 20)

        # размер доски без полей
        self.board_size = min_dim - 2 * self.margin
        self.square_size = self.board_size // 8

        # центрирование доски
        self.start_x = (screen_w - self.board_size) // 2
        self.start_y = (screen_h - self.board_size) // 2

        # динамический размер шрифта
        pygame.font.init()
        font_size = max(int(self.margin * 0.4), 12)
        self.coord_font = pygame.font.SysFont("Arial", font_size, bold=True)

        # загрузка и масштабирование картинок фигур
        self._load_images()

    # загружает картинки фигур
    def _load_images(self):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        img_dir = os.path.join(base_dir, "assets", "images")
        pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        colors = ["w", "b"]

        for color in colors:
            for piece in pieces:
                piece_name = f"{color}_{piece}"
                img_path = os.path.join(img_dir, f"{piece_name}.png")
                try:
                    img = pygame.image.load(img_path)
                    # сглаживание для лучшего качества
                    img = pygame.transform.smoothscale(
                        img, (self.square_size, self.square_size)
                    )
                    self.images[piece_name] = img
                except Exception as e:
                    print(f"Ошибка загрузки {img_path}: {e}")

    # запускает анимацию движения фигуры
    def start_animation(self, start_logical_pos, end_logical_pos, dying_info=None):
        """Запускает анимацию скольжения фигуры."""
        row_e, col_e = end_logical_pos
        row_s, col_s = start_logical_pos

        # вычисляем пиксельные координаты
        start_x = self.start_x + col_s * self.square_size
        start_y = self.start_y + row_s * self.square_size
        end_x = self.start_x + col_e * self.square_size
        end_y = self.start_y + row_e * self.square_size

        # сохраняем параметры анимации
        self.anim_start_pos = (start_x, start_y)
        self.anim_end_pos = (end_x, end_y)
        self.anim_current_frame = 0
        self.is_animating = True
        self.dying_info = dying_info

    # рисует шахматную доску
    def draw_board(self, board, flip_board=False, selected_square=None):
        # фон вокруг доски
        bg_color = (
            max(self.dark_color[0] - 40, 0),
            max(self.dark_color[1] - 40, 0),
            max(self.dark_color[2] - 40, 0),
        )
        bg_rect = pygame.Rect(
            self.start_x - self.margin,
            self.start_y - self.margin,
            self.board_size + self.margin * 2,
            self.board_size + self.margin * 2,
        )

        pygame.draw.rect(self.screen, bg_color, bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect, width=3, border_radius=5)

        # рисуем клетки
        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = self.light_color if is_light else self.dark_color

                piece = board.grid[row][col]

                # проверка на шах
                if (
                    piece is not None
                    and piece.name == "king"
                    and board.is_in_check(piece.color)
                ):
                    # плавная пульсация цвета
                    time_ticks = pygame.time.get_ticks()
                    pulse = (
                        math.sin(time_ticks / 200.0) + 1
                    ) / 2.0  # значение от 0 до 1

                    # смешивание цвета клетки с красным
                    base_c = self.light_color if is_light else self.dark_color
                    color = (
                        int(base_c[0] + (220 - base_c[0]) * pulse),
                        int(base_c[1] + (50 - base_c[1]) * pulse),
                        int(base_c[2] + (50 - base_c[2]) * pulse),
                    )
                # подсветка выбранной клетки
                elif selected_square == (row, col):
                    color = (173, 216, 230)

                # переворачиваем координаты, если нужно
                draw_row = 7 - row if flip_board else row
                draw_col = 7 - col if flip_board else col

                # рисуем саму клетку
                x = self.start_x + draw_col * self.square_size
                y = self.start_y + draw_row * self.square_size

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x, y, self.square_size, self.square_size),
                )

        # рамка самой доски
        board_rect = pygame.Rect(
            self.start_x, self.start_y, self.board_size, self.board_size
        )
        pygame.draw.rect(self.screen, (0, 0, 0), board_rect, width=2)

    # рисует координаты по бокам доски
    def draw_coordinates(self, flip_board=False):
        """Рисует координаты со всех четырех сторон доски."""
        current_files = self.files[::-1] if flip_board else self.files
        current_ranks = self.ranks[::-1] if flip_board else self.ranks

        # цвет текста под светлые клетки
        text_color = self.light_color

        for i in range(8):
            # цифры рядов (1-8)
            text_num = self.coord_font.render(current_ranks[i], True, text_color)

            left_rect = text_num.get_rect(
                center=(
                    self.start_x - self.margin // 2,
                    self.start_y + i * self.square_size + self.square_size // 2,
                )
            )
            self.screen.blit(text_num, left_rect)

            right_rect = text_num.get_rect(
                center=(
                    self.start_x + self.board_size + self.margin // 2,
                    self.start_y + i * self.square_size + self.square_size // 2,
                )
            )
            self.screen.blit(text_num, right_rect)

            # буквы линий (a-h)
            text_let = self.coord_font.render(current_files[i], True, text_color)

            bottom_rect = text_let.get_rect(
                center=(
                    self.start_x + i * self.square_size + self.square_size // 2,
                    self.start_y + self.board_size + self.margin // 2,
                )
            )
            self.screen.blit(text_let, bottom_rect)

            top_rect = text_let.get_rect(
                center=(
                    self.start_x + i * self.square_size + self.square_size // 2,
                    self.start_y - self.margin // 2,
                )
            )
            self.screen.blit(text_let, top_rect)

    # рисует фигуры на доске
    def draw_pieces(self, board, flip_board=False):
        animating_piece_name = None
        current_anim_x, current_anim_y = 0, 0

        # расчет координат для анимации
        if self.is_animating:
            self.anim_current_frame += 1
            progress = self.anim_current_frame / self.anim_total_frames

            # линейная интерполяция для плавного движения
            current_anim_x = (
                self.anim_start_pos[0]
                + (self.anim_end_pos[0] - self.anim_start_pos[0]) * progress
            )
            current_anim_y = (
                self.anim_start_pos[1]
                + (self.anim_end_pos[1] - self.anim_start_pos[1]) * progress
            )

            # определяем имя анимируемой фигуры
            finish_col = (self.anim_end_pos[0] - self.start_x) // self.square_size
            finish_row = (self.anim_end_pos[1] - self.start_y) // self.square_size
            p = board.grid[finish_row][finish_col]
            if p:
                animating_piece_name = str(p)

            # завершаем анимацию
            if self.anim_current_frame >= self.anim_total_frames:
                self.is_animating = False

        # отрисовка статичных фигур
        for row in range(8):
            for col in range(8):
                piece = board.grid[row][col]
                if piece is not None:
                    # пропуск летящей фигуры, чтобы нарисовать ее позже
                    if self.is_animating and (
                        self.anim_end_pos
                        == (
                            self.start_x + col * self.square_size,
                            self.start_y + row * self.square_size,
                        )
                    ):
                        continue

                    draw_row = 7 - row if flip_board else row
                    draw_col = 7 - col if flip_board else col

                    x = self.start_x + draw_col * self.square_size
                    y = self.start_y + draw_row * self.square_size

                    piece_key = str(piece)
                    if piece_key in self.images:
                        self.screen.blit(
                            self.images[piece_key],
                            pygame.Rect(x, y, self.square_size, self.square_size),
                        )

        # анимация исчезновения срубленной фигуры
        if self.is_animating and self.dying_info:
            d_name, (d_row, d_col) = self.dying_info
            if d_name in self.images:
                dying_img = self.images[d_name].copy()
                # расчет прозрачности для исчезновения
                alpha = max(
                    0,
                    255 - int(255 * (self.anim_current_frame / self.anim_total_frames)),
                )
                dying_img.set_alpha(alpha)

                # расчет координат
                draw_row = 7 - d_row if flip_board else d_row
                draw_col = 7 - d_col if flip_board else d_col
                dying_x = self.start_x + draw_col * self.square_size
                dying_y = self.start_y + draw_row * self.square_size

                self.screen.blit(dying_img, (dying_x, dying_y))

        # отрисовка летящей фигуры поверх всех
        if (
            self.is_animating
            and animating_piece_name
            and animating_piece_name in self.images
        ):
            img = self.images[animating_piece_name]

            # специальный расчет для перевернутой доски
            if flip_board:
                center_x = self.start_x + self.board_size // 2
                center_y = self.start_y + self.board_size // 2
                draw_x = (
                    center_x
                    - (current_anim_x + self.square_size // 2 - center_x)
                    - self.square_size // 2
                )
                draw_y = (
                    center_y
                    - (current_anim_y + self.square_size // 2 - center_y)
                    - self.square_size // 2
                )
            else:
                draw_x, draw_y = current_anim_x, current_anim_y

            self.screen.blit(img, (draw_x, draw_y))

    # рисует подсказки для ходов
    def draw_move_hints(self, valid_moves, board, flip_board=False):
        hint_color = tuple(
            self.config_manager.get_board_settings().get(
                "move_hint_color", [144, 238, 144]
            )
        )
        for row, col in valid_moves:
            draw_row = 7 - row if flip_board else row
            draw_col = 7 - col if flip_board else col

            x = self.start_x + draw_col * self.square_size
            y = self.start_y + draw_row * self.square_size

            # если клетка пустая, рисуем кружок
            if board.grid[row][col] is None:
                center_x = x + self.square_size // 2
                center_y = y + self.square_size // 2
                # радиус зависит от размера клетки
                pygame.draw.circle(
                    self.screen,
                    hint_color,
                    (center_x, center_y),
                    max(self.square_size // 6, 5),
                )
            # если на клетке враг, рисуем рамку
            else:
                # толщина рамки зависит от клетки
                pygame.draw.rect(
                    self.screen,
                    hint_color,
                    pygame.Rect(x, y, self.square_size, self.square_size),
                    width=max(self.square_size // 20, 2),
                )
