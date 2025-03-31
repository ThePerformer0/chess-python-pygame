# main.py
from game import Board

if __name__ == "__main__":
    game_board = Board()
    print(f"Est-ce que le coup de (0, 0) à (3, 3) est valide ? {game_board.is_valid_move(0, 0, 3, 3)}")
    print(f"Est-ce que le coup de (0, 0) à (8, 8) est valide ? {game_board.is_valid_move(0, 0, 8, 8)}")