# board.py
from pieces import *

class Board:
    def __init__(self):
        """Initialise le plateau de jeu avec les pièces à leurs positions de départ."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialiser_plateau()

    def initialiser_plateau(self):
        """Place les pièces à leurs positions de départ sur le plateau."""
        # Pièces noires
        self.board[0][0] = Rook('noir', (0, 0))
        self.board[0][1] = Knight('noir', (0, 1))
        self.board[0][2] = Bishop('noir', (0, 2))
        self.board[0][3] = Queen('noir', (0, 3))
        self.board[0][4] = King('noir', (0, 4))
        self.board[0][5] = Bishop('noir', (0, 5))
        self.board[0][6] = Knight('noir', (0, 6))
        self.board[0][7] = Rook('noir', (0, 7))
        for i in range(8):
            self.board[1][i] = Pawn('noir', (1, i))

        # Pièces blanches
        self.board[7][0] = Rook('blanc', (7, 0))
        self.board[7][1] = Knight('blanc', (7, 1))
        self.board[7][2] = Bishop('blanc', (7, 2))
        self.board[7][3] = Queen('blanc', (7, 3))
        self.board[7][4] = King('blanc', (7, 4))
        self.board[7][5] = Bishop('blanc', (7, 5))
        self.board[7][6] = Knight('blanc', (7, 6))
        self.board[7][7] = Rook('blanc', (7, 7))
        for i in range(8):
            self.board[6][i] = Pawn('blanc', (6, i))

    def obtenir_piece(self, position):
        """Retourne l'objet Piece à une position donnée (ligne, colonne)."""
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def placer_piece(self, piece, position):
        """Place un objet Piece à une position donnée (ligne, colonne)."""
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
            if piece:
                piece.position = position

    def deplacer_piece(self, depart, arrivee):
        """Déplace une pièce de la position de départ à la position d'arrivée."""
        piece = self.obtenir_piece(depart)
        if piece:
            self.board[depart[0]][depart[1]] = None
            self.placer_piece(piece, arrivee)
            if isinstance(piece, Pawn):
                piece.premier_mouvement = False # Marquer le premier mouvement du pion comme terminé

    def est_mouvement_valide(self, depart, arrivee):
        """Vérifie si le mouvement de la position de départ à la position d'arrivée est valide."""
        piece = self.obtenir_piece(depart)
        if piece is None:
            return False

        mouvements_possibles = piece.mouvements_valides(self.board)
        return arrivee in mouvements_possibles

    # Méthode pour l'affichage en console (pour le débogage)
    def afficher_plateau(self):
        """Affiche l'état actuel du plateau dans la console."""
        notation_ligne = ['8', '7', '6', '5', '4', '3', '2', '1']
        notation_colonne = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        print("  a b c d e f g h")
        print("  ---------------")
        for i in range(8):
            ligne = notation_ligne[i] + "| "
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    ligne += ". "
                else:
                    couleur = 'W' if piece.couleur == 'blanc' else 'B'
                    type_abbr = piece.type[0].upper()
                    if piece.type == 'cavalier':
                        type_abbr = 'N'
                    ligne += couleur + type_abbr + " "
            print(ligne)