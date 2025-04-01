# pieces.py

class Piece:
    def __init__(self, couleur, position, type):
        """
        Initialise une pièce d'échecs.

        Args:
            couleur (str): La couleur de la pièce ('blanc' ou 'noir').
            position (tuple): La position de la pièce sur le plateau (ligne, colonne).
            type (str): Le type de la pièce ('pion', 'tour', 'cavalier', 'fou', 'reine', 'roi').
        """
        self.couleur = couleur
        self.position = position
        self.type = type

    def mouvements_valides(self, plateau):
        """
        Méthode abstraite pour retourner les mouvements valides de la pièce.
        Doit être implémentée par les sous-classes.

        Args:
            plateau (list[list]): Une représentation 2D du plateau de jeu.

        Returns:
            list[tuple]: Une liste des positions (ligne, colonne) vers lesquelles la pièce peut se déplacer.
        """
        raise NotImplementedError("La méthode mouvements_valides doit être implémentée par la sous-classe.")
    
class Pawn(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'pion')

    def mouvements_valides(self, plateau):
        # La logique spécifique au mouvement du pion sera implémentée ici
        return []

class Rook(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'tour')

    def mouvements_valides(self, plateau):
        # La logique spécifique au mouvement de la tour sera implémentée ici
        return []

class Knight(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'cavalier')

    def mouvements_valides(self, plateau):
        # La logique spécifique au mouvement du cavalier sera implémentée ici
        return []

class Bishop(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'fou')

    def mouvements_valides(self, plateau):
        # La logique spécifique au mouvement du fou sera implémentée ici
        return []

class Queen(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'reine')

    def mouvements_valides(self, plateau):
        # La logique spécifique au mouvement de la reine sera implémentée ici
        return []

class King(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'roi')

    def mouvements_valides(self, plateau):
        # La logique spécifique au mouvement du roi sera implémentée ici
        return []