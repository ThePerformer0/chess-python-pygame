# game.py

class Board:
    def __init__(self):
        self.board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]
        self.initialize_board()

    def initialize_board(self):
        # Placement des pièces blanches
        self.board[7][0] = "wr"  # Tour blanche
        self.board[7][1] = "wn"  # Cavalier blanc
        self.board[7][2] = "wb"  # Fou blanc
        self.board[7][3] = "wq"  # Dame blanche
        self.board[7][4] = "wk"  # Roi blanc
        self.board[7][5] = "wb"  # Fou blanc
        self.board[7][6] = "wn"  # Cavalier blanc
        self.board[7][7] = "wr"  # Tour blanche
        for i in range(8):
            self.board[6][i] = "wp"  # Pions blancs

        # Placement des pièces noires
        self.board[0][0] = "br"  # Tour noire
        self.board[0][1] = "bn"  # Cavalier noir
        self.board[0][2] = "bb"  # Fou noir
        self.board[0][3] = "bq"  # Dame noire
        self.board[0][4] = "bk"  # Roi noir
        self.board[0][5] = "bb"  # Fou noir
        self.board[0][6] = "bn"  # Cavalier noir
        self.board[0][7] = "br"  # Tour noire
        for i in range(8):
            self.board[1][i] = "bp"  # Pions noirs

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def set_piece(self, row, col, piece):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += " ".join(str(piece).ljust(2) if piece else "  " for piece in row) + "\n"
        return board_str

if __name__ == "__main__":
    board = Board()
    print(board)