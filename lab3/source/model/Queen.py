from .Piece import Piece


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "queen")

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
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_piece = board.grid[r][c]
                if target_piece is None:
                    moves.append((r, c))
                elif target_piece.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves
