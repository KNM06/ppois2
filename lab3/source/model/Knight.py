from .Piece import Piece


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "knight")

    def get_possible_moves(self, board, current_pos):
        moves = []
        row, col = current_pos
        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board.grid[r][c]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((r, c))
        return moves
