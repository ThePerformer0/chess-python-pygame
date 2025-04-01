from board import Board
from pieces import King, Pawn, Queen

class Game:
    def __init__(self):
        self.board = Board()
        self.tour_blanc = True
        self.piece_selectionnee = None
        self.partie_terminee = False
        self.dernier_mouvement = None  # Pour la prise en passant
        self.en_echec = False
        
    def selectionner_piece(self, position):
        piece = self.board.obtenir_piece(position)
        if piece and piece.couleur == ('blanc' if self.tour_blanc else 'noir'):
            self.piece_selectionnee = position
            return True
        return False
        
    def est_en_echec(self, couleur):
        """Vérifie si le roi de la couleur donnée est en échec"""
        # Trouver le roi
        position_roi = None
        for i in range(8):
            for j in range(8):
                piece = self.board.obtenir_piece((i, j))
                if isinstance(piece, King) and piece.couleur == couleur:
                    position_roi = (i, j)
                    break
            if position_roi:
                break
                
        # Vérifier si une pièce adverse peut attaquer le roi
        for i in range(8):
            for j in range(8):
                piece = self.board.obtenir_piece((i, j))
                if piece and piece.couleur != couleur:
                    mouvements = piece.mouvements_valides(self.board.board)
                    if position_roi in mouvements:
                        return True
        return False
        
    def est_en_echec_et_mat(self, couleur):
        """Vérifie si le roi de la couleur donnée est en échec et mat"""
        if not self.est_en_echec(couleur):
            return False
            
        # Essayer tous les mouvements possibles pour chaque pièce
        for i in range(8):
            for j in range(8):
                piece = self.board.obtenir_piece((i, j))
                if piece and piece.couleur == couleur:
                    mouvements = piece.mouvements_valides(self.board.board)
                    position_originale = piece.position
                    
                    for mouvement in mouvements:
                        # Sauvegarder l'état actuel
                        piece_capturee = self.board.obtenir_piece(mouvement)
                        
                        # Essayer le mouvement
                        self.board.deplacer_piece(position_originale, mouvement)
                        
                        # Vérifier si on est toujours en échec
                        toujours_en_echec = self.est_en_echec(couleur)
                        
                        # Annuler le mouvement
                        self.board.deplacer_piece(mouvement, position_originale)
                        if piece_capturee:
                            self.board.placer_piece(piece_capturee, mouvement)
                            
                        if not toujours_en_echec:
                            return False
                            
        return True
        
    def mouvement_met_en_echec(self, depart, arrivee, couleur):
        """Vérifie si un mouvement met le roi en échec"""
        piece = self.board.obtenir_piece(depart)
        piece_capturee = self.board.obtenir_piece(arrivee)
        
        # Essayer le mouvement
        self.board.deplacer_piece(depart, arrivee)
        en_echec = self.est_en_echec(couleur)
        
        # Annuler le mouvement
        self.board.deplacer_piece(arrivee, depart)
        if piece_capturee:
            self.board.placer_piece(piece_capturee, arrivee)
            
        return en_echec

    def deplacer_piece(self, position_arrivee):
        if not self.piece_selectionnee:
            return False

        depart = self.piece_selectionnee
        piece = self.board.obtenir_piece(depart)
        
        if not piece or not self.board.est_mouvement_valide(depart, position_arrivee):
            return False
            
        # Vérifier si le mouvement met le roi en échec
        if self.mouvement_met_en_echec(depart, position_arrivee, piece.couleur):
            return False

        # Gestion du roque
        if isinstance(piece, King) and abs(depart[1] - position_arrivee[1]) == 2:
            if self.est_en_echec(piece.couleur):
                return False
            self._executer_roque(depart, position_arrivee)
            return True

        # Gestion de la prise en passant
        if isinstance(piece, Pawn):
            if abs(depart[1] - position_arrivee[1]) == 1 and self.board.obtenir_piece(position_arrivee) is None:
                self._executer_prise_en_passant(depart, position_arrivee)
                return True

        # Mouvement normal
        self.board.deplacer_piece(depart, position_arrivee)

        # Mise à jour pour la prise en passant
        if isinstance(piece, Pawn) and abs(depart[0] - position_arrivee[0]) == 2:
            piece.peut_etre_pris_en_passant = True
        else:
            self._reset_prise_en_passant()

        # Gestion de la promotion
        if isinstance(piece, Pawn) and (position_arrivee[0] == 0 or position_arrivee[0] == 7):
            self._promouvoir_pion(position_arrivee)

        self.tour_blanc = not self.tour_blanc
        self.piece_selectionnee = None

        # Vérifier l'échec et mat après le mouvement
        couleur_adverse = 'noir' if self.tour_blanc else 'blanc'
        if self.est_en_echec(couleur_adverse):
            self.en_echec = True
            if self.est_en_echec_et_mat(couleur_adverse):
                self.partie_terminee = True

        return True

    def _executer_roque(self, depart, arrivee):
        roi = self.board.obtenir_piece(depart)
        # Petit roque
        if arrivee[1] > depart[1]:
            tour_depart = (depart[0], 7)
            tour_arrivee = (depart[0], arrivee[1] - 1)
        # Grand roque
        else:
            tour_depart = (depart[0], 0)
            tour_arrivee = (depart[0], arrivee[1] + 1)

        # Déplacer le roi et la tour
        self.board.deplacer_piece(depart, arrivee)
        self.board.deplacer_piece(tour_depart, tour_arrivee)
        roi.a_bouge = True

    def _executer_prise_en_passant(self, depart, arrivee):
        # Supprimer le pion capturé
        pion_capture = (depart[0], arrivee[1])
        self.board.placer_piece(None, pion_capture)
        # Déplacer le pion qui capture
        self.board.deplacer_piece(depart, arrivee)

    def _reset_prise_en_passant(self):
        for i in range(8):
            for j in range(8):
                piece = self.board.obtenir_piece((i, j))
                if isinstance(piece, Pawn):
                    piece.peut_etre_pris_en_passant = False

    def _promouvoir_pion(self, position):
        # Par défaut, on promeut en Dame
        couleur = 'blanc' if self.tour_blanc else 'noir'
        self.board.placer_piece(Queen(couleur, position), position)
