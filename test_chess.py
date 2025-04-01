import pygame
from gui import GUI
from game import Game

def test_mouvements_piece():
    """Test des mouvements possibles d'une pièce"""
    game = Game()
    # Test du pion
    piece = game.board.obtenir_piece((6, 0))  # Pion blanc
    mouvements = piece.mouvements_valides(game.board.board)
    print(f"Mouvements possibles du pion: {mouvements}")
    
    # Test de la tour
    piece = game.board.obtenir_piece((7, 0))  # Tour blanche
    mouvements = piece.mouvements_valides(game.board.board)
    print(f"Mouvements possibles de la tour: {mouvements}")

def test_interface():
    """Test de l'interface graphique"""
    gui = GUI()
    gui.run()

def main():
    # Exécuter les tests
    print("Test des mouvements...")
    test_mouvements_piece()
    
    print("\nLancement de l'interface graphique...")
    test_interface()

if __name__ == "__main__":
    main() 