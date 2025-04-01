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
        self.premier_mouvement = True
        self.peut_etre_pris_en_passant = False

    def mouvements_valides(self, plateau):
        mouvements = []
        x, y = self.position
        direction = -1 if self.couleur == 'blanc' else 1
        
        # Mouvement simple
        if 0 <= x + direction < 8 and plateau[x + direction][y] is None:
            mouvements.append((x + direction, y))
            # Double mouvement au premier tour
            if self.premier_mouvement and plateau[x + 2*direction][y] is None:
                mouvements.append((x + 2*direction, y))
        
        # Captures normales en diagonale
        for dy in [-1, 1]:
            if 0 <= x + direction < 8 and 0 <= y + dy < 8:
                case_cible = plateau[x + direction][y + dy]
                if case_cible is not None and case_cible.couleur != self.couleur:
                    mouvements.append((x + direction, y + dy))

        # Prise en passant
        if (self.couleur == 'blanc' and x == 3) or (self.couleur == 'noir' and x == 4):
            for dy in [-1, 1]:
                if 0 <= y + dy < 8:
                    piece_adjacente = plateau[x][y + dy]
                    if (isinstance(piece_adjacente, Pawn) and 
                        piece_adjacente.couleur != self.couleur and 
                        piece_adjacente.peut_etre_pris_en_passant):
                        mouvements.append((x + direction, y + dy))
        
        return mouvements

class Rook(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'tour')
        self.a_bouge = False  # Pour le roque

    def mouvements_valides(self, plateau):
        mouvements = []
        x, y = self.position
        # Directions : haut, bas, gauche, droite
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if plateau[nx][ny] is None:
                    mouvements.append((nx, ny))
                elif plateau[nx][ny].couleur != self.couleur:
                    mouvements.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
                
        return mouvements

class Knight(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'cavalier')

    def mouvements_valides(self, plateau):
        mouvements = []
        x, y = self.position
        # Tous les mouvements possibles du cavalier en L
        deplacements = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dx, dy in deplacements:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if plateau[nx][ny] is None or plateau[nx][ny].couleur != self.couleur:
                    mouvements.append((nx, ny))
                    
        return mouvements

class Bishop(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'fou')

    def mouvements_valides(self, plateau):
        mouvements = []
        x, y = self.position
        # Directions diagonales
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if plateau[nx][ny] is None:
                    mouvements.append((nx, ny))
                elif plateau[nx][ny].couleur != self.couleur:
                    mouvements.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
                
        return mouvements

class Queen(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'reine')

    def mouvements_valides(self, plateau):
        mouvements = []
        x, y = self.position
        # Combine les mouvements de la tour et du fou
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if plateau[nx][ny] is None:
                    mouvements.append((nx, ny))
                elif plateau[nx][ny].couleur != self.couleur:
                    mouvements.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
                
        return mouvements

class King(Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position, 'roi')
        self.a_bouge = False  # Pour le roque

    def mouvements_valides(self, plateau):
        mouvements = []
        x, y = self.position
        # Mouvements normaux
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if plateau[nx][ny] is None or plateau[nx][ny].couleur != self.couleur:
                    mouvements.append((nx, ny))

        # Roque
        if not self.a_bouge:
            # Petit roque
            if self._peut_faire_petit_roque(plateau):
                mouvements.append((x, y + 2))
            # Grand roque
            if self._peut_faire_grand_roque(plateau):
                mouvements.append((x, y - 2))

        return mouvements

    def _peut_faire_petit_roque(self, plateau):
        x, y = self.position
        # Vérifier si la tour est à sa position initiale
        tour_position = plateau[x][7]
        if not isinstance(tour_position, Rook) or tour_position.a_bouge:
            return False
        # Vérifier si les cases entre le roi et la tour sont vides
        return all(plateau[x][i] is None for i in range(y + 1, 7))

    def _peut_faire_grand_roque(self, plateau):
        x, y = self.position
        # Vérifier si la tour est à sa position initiale
        tour_position = plateau[x][0]
        if not isinstance(tour_position, Rook) or tour_position.a_bouge:
            return False
        # Vérifier si les cases entre le roi et la tour sont vides
        return all(plateau[x][i] is None for i in range(1, y))