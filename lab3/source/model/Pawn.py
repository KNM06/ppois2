from .Piece import Piece


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn")

    def get_possible_moves(self, board, current_pos):
        moves = []
        row, col = current_pos
        direction = -1 if self.color == "w" else 1
        start_row = 6 if self.color == "w" else 1

        # 1. Шаг вперед
        r = row + direction
        if 0 <= r < 8 and board.grid[r][col] is None:
            moves.append((r, col))
            # 2. Двойной шаг
            if row == start_row:
                r2 = row + 2 * direction
                if board.grid[r2][col] is None:
                    moves.append((r2, col))

        # 3. Взятие по диагонали
        for dc in [-1, 1]:
            c = col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board.grid[r][c]
                if target_piece is not None and target_piece.color != self.color:
                    moves.append((r, c))
                # 4. ВЗЯТИЕ НА ПРОХОДЕ
                elif board.last_move is not None:
                    last_start, last_end, last_piece = board.last_move
                    # Проверяем, ходила ли вражеская пешка на 2 клетки рядом с нами
                    if last_piece.name == "pawn" and last_piece.color != self.color:
                        if abs(last_start[0] - last_end[0]) == 2:
                            if last_end[0] == row and last_end[1] == c:
                                moves.append((r, c))
        return moves
