class GameController:
    def __init__(self, model, view, sound_manager=None):
        self.model = model
        self.view = view
        self.sound_manager = sound_manager
        self.selected_square = None
        self.valid_moves = []

        # данные для онлайн игры
        self.network = None
        self.my_color = "both"  # 'both' - локально, 'w'/'b' - онлайн
        self.incoming_moves = []

    # обновляет игру, обрабатывая ходы из сети
    def update(self):
        """Метод вызывается каждый кадр в main.py. Обрабатывает ходы из сети."""
        while self.incoming_moves:
            start_pos, end_pos = self.incoming_moves.pop(0)
            self._apply_move(start_pos, end_pos, is_network=True)

    # применяет ход, запуская анимацию и звуки
    def _apply_move(self, start_pos, end_pos, is_network=False):
        """Единая логика перемещения, анимации и звуков."""
        target_piece = self.model.grid[end_pos[0]][end_pos[1]]
        moving_piece = self.model.grid[start_pos[0]][start_pos[1]]

        # проверка на взятие фигуры
        is_capture = target_piece is not None
        dying_info = None
        if target_piece:
            dying_info = (str(target_piece), end_pos)
        # проверка на взятие на проходе
        elif (
            moving_piece.name == "pawn"
            and start_pos[1] != end_pos[1]
            and target_piece is None
        ):
            is_capture = True
            ep_piece = self.model.grid[start_pos[0]][end_pos[1]]
            if ep_piece:
                dying_info = (str(ep_piece), (start_pos[0], end_pos[1]))

        # двигаем фигуру в модели
        old_logical_pos = self.model.move_piece(start_pos, end_pos)
        # запускаем анимацию
        self.view.start_animation(old_logical_pos, end_pos, dying_info)

        # проигрываем звуки
        if self.sound_manager:
            if self.model.game_over and self.model.winner != "draw":
                self.sound_manager.play_checkmate()
            elif is_capture:
                self.sound_manager.play_capture()
            else:
                self.sound_manager.play_move()

        # если ход наш, отправляем его на сервер
        if not is_network and self.network:
            self.network.send_move(start_pos, end_pos)

    # обрабатывает клики мыши по доске
    def handle_mouse_click(self, mouse_pos, flip_board):
        # если игра окончена, ничего не делаем
        if self.model.game_over:
            return

        # в онлайне блокируем ход, если не наша очередь
        if self.my_color != "both" and self.model.current_turn != self.my_color:
            return

        # конвертируем пиксели в координаты доски
        x, y = mouse_pos
        board_x = x - self.view.start_x
        board_y = y - self.view.start_y

        # если клик за пределами доски, сбрасываем выделение
        if (
            board_x < 0
            or board_y < 0
            or board_x >= self.view.board_size
            or board_y >= self.view.board_size
        ):
            self.selected_square = None
            self.valid_moves = []
            return

        # получаем строку и столбец
        col = board_x // self.view.square_size
        row = board_y // self.view.square_size

        # переворачиваем координаты, если доска перевернута
        if flip_board:
            col, row = 7 - col, 7 - row

        # если клетка уже выбрана
        if self.selected_square:
            # если кликнули на ту же клетку, снимаем выделение
            if self.selected_square == (row, col):
                self.selected_square = None
                self.valid_moves = []
            # если кликнули на валидный ход, делаем ход
            elif (row, col) in self.valid_moves:
                self._apply_move(self.selected_square, (row, col))
                self.selected_square = None
                self.valid_moves = []
            # если кликнули на другую клетку, сбрасываем выделение
            else:
                self.selected_square = None
                self.valid_moves = []
        # если клетка не выбрана
        else:
            piece = self.model.grid[row][col]
            # если на клетке есть наша фигура, выделяем ее
            if piece is not None and piece.color == self.model.current_turn:
                self.selected_square = (row, col)
                self.valid_moves = self.model.get_legal_moves((row, col))
