class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.has_moved = False

    def __str__(self):
        return f"{self.color}_{self.name}"

    def get_possible_moves(self, board, current_pos):
        return []
