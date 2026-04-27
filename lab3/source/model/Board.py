from .Knight import Knight
from .Rook import Rook
from .Bishop import Bishop
from .Queen import Queen
from .King import King
from .Pawn import Pawn


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "w"
        self.game_over = False
        self.winner = None
        self.last_move = None  # Запоминаем последний ход для взятия на проходе
        self._setup_board()

    def _setup_board(self):
        self.grid[0] = [
            Rook("b"),
            Knight("b"),
            Bishop("b"),
            Queen("b"),
            King("b"),
            Bishop("b"),
            Knight("b"),
            Rook("b"),
        ]
        self.grid[1] = [Pawn("b") for _ in range(8)]
        self.grid[6] = [Pawn("w") for _ in range(8)]
        self.grid[7] = [
            Rook("w"),
            Knight("w"),
            Bishop("w"),
            Queen("w"),
            King("w"),
            Bishop("w"),
            Knight("w"),
            Rook("w"),
        ]

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.grid[start_row][start_col]

        is_castling = piece.name == "king" and abs(start_col - end_col) == 2
        is_en_passant = (
            piece.name == "pawn"
            and start_col != end_col
            and self.grid[end_row][end_col] is None
        )

        # Перемещаем главную фигуру
        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = None

        # --- ЛОГИКА РОКИРОВКИ (Двигаем ладью) ---
        if is_castling:
            if end_col == 6:  # Короткая
                rook = self.grid[start_row][7]
                self.grid[start_row][5] = rook
                self.grid[start_row][7] = None
                rook.has_moved = True
            elif end_col == 2:  # Длинная
                rook = self.grid[start_row][0]
                self.grid[start_row][3] = rook
                self.grid[start_row][0] = None
                rook.has_moved = True

        # --- ЛОГИКА ВЗЯТИЯ НА ПРОХОДЕ ---
        if is_en_passant:
            self.grid[start_row][end_col] = None

        piece.has_moved = True

        if piece.name == "pawn":
            if (piece.color == "w" and end_row == 0) or (
                piece.color == "b" and end_row == 7
            ):
                self.grid[end_row][end_col] = Queen(piece.color)

        self.last_move = (start_pos, end_pos, piece)
        self.current_turn = "b" if self.current_turn == "w" else "w"
        self.check_game_over()

        # --- НОВОЕ: Возвращаем старую позицию для анимации ---
        return start_pos

    def is_in_check(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None and p.name == "king" and p.color == color:
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None and p.color != color:
                    if king_pos in p.get_possible_moves(self, (r, c)):
                        return True
        return False

    def get_legal_moves(self, pos):
        r, c = pos
        piece = self.grid[r][c]
        if piece is None:
            return []

        pseudo_moves = piece.get_possible_moves(self, pos)
        legal_moves = []

        for end_pos in pseudo_moves:
            end_r, end_c = end_pos
            target_piece = self.grid[end_r][end_c]

            # --- ВИРТУАЛЬНАЯ ПРОВЕРКА ДЛЯ ВЗЯТИЯ НА ПРОХОДЕ ---
            is_en_passant = False
            ep_captured_pawn = None
            if piece.name == "pawn" and c != end_c and target_piece is None:
                is_en_passant = True
                ep_captured_pawn = self.grid[r][end_c]
                self.grid[r][end_c] = None  # Временно убираем сбитую пешку

            # --- ВИРТУАЛЬНАЯ ПРОВЕРКА ДЛЯ РОКИРОВКИ ---
            if piece.name == "king" and abs(c - end_c) == 2:
                if self.is_in_check(piece.color):
                    continue  # Нельзя рокироваться из-под шаха

                step = 1 if end_c > c else -1
                passing_c = c + step
                # Временно ставим короля на пробиваемое поле
                self.grid[r][passing_c] = piece
                self.grid[r][c] = None
                passing_in_check = self.is_in_check(piece.color)
                self.grid[r][c] = piece
                self.grid[r][passing_c] = None

                if passing_in_check:
                    continue  # Нельзя рокироваться через битое поле

            # --- БАЗОВЫЙ ВИРТУАЛЬНЫЙ ХОД ---
            self.grid[end_r][end_c] = piece
            self.grid[r][c] = None

            if not self.is_in_check(piece.color):
                legal_moves.append(end_pos)

            # --- ОТКАТ ХОДА ---
            self.grid[r][c] = piece
            self.grid[end_r][end_c] = target_piece

            if is_en_passant:
                self.grid[r][end_c] = ep_captured_pawn  # Возвращаем пешку на место

        return legal_moves

    def check_game_over(self):
        has_moves = False
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece is not None and piece.color == self.current_turn:
                    if len(self.get_legal_moves((r, c))) > 0:
                        has_moves = True
                        break
            if has_moves:
                break

        if not has_moves:
            self.game_over = True
            if self.is_in_check(self.current_turn):
                self.winner = "w" if self.current_turn == "b" else "b"
            else:
                self.winner = "draw"
