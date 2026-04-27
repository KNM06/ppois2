from .Piece import Piece


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "king")

    def get_possible_moves(self, board, current_pos):
        moves = []
        row, col = current_pos
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        # 1. Обычные шаги
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board.grid[r][c]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((r, c))

        # 2. РОКИРОВКА (Псевдолегальная проверка)
        if not self.has_moved:
            # Короткая (на королевский фланг)
            if board.grid[row][5] is None and board.grid[row][6] is None:
                rook = board.grid[row][7]
                if rook is not None and rook.name == "rook" and not rook.has_moved:
                    moves.append((row, 6))
            # Длинная (на ферзевый фланг)
            if (
                board.grid[row][1] is None
                and board.grid[row][2] is None
                and board.grid[row][3] is None
            ):
                rook = board.grid[row][0]
                if rook is not None and rook.name == "rook" and not rook.has_moved:
                    moves.append((row, 2))

        return moves
