class ChessAI:
    def __init__(self, couleur):
        self.couleur = couleur
        self.valeurs_pieces = {
            'pion': 1,
            'cavalier': 3,
            'fou': 3,
            'tour': 5,
            'reine': 9,
            'roi': 100
        }

    def evaluer_position(self, board):
        """Évalue la position actuelle du plateau"""
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board.obtenir_piece((i, j))
                if piece:
                    # Score positif pour les pièces de l'IA, négatif pour l'adversaire
                    multiplicateur = 1 if piece.couleur == self.couleur else -1
                    score += self.valeurs_pieces[piece.type] * multiplicateur
                    
                    # Bonus pour les pions avancés
                    if piece.type == 'pion':
                        if piece.couleur == self.couleur:
                            score += (7 - i) * 0.1 if self.couleur == 'blanc' else i * 0.1
        return score

    def obtenir_tous_mouvements(self, board, couleur):
        """Obtient tous les mouvements possibles pour une couleur"""
        mouvements = []
        for i in range(8):
            for j in range(8):
                piece = board.obtenir_piece((i, j))
                if piece and piece.couleur == couleur:
                    for mouvement in piece.mouvements_valides(board.board):
                        mouvements.append(((i, j), mouvement))
        return mouvements

    def choisir_mouvement(self, game):
        """Choisit le meilleur mouvement selon l'évaluation simple"""
        meilleur_score = float('-inf')
        meilleur_mouvement = None
        
        # Obtenir tous les mouvements possibles
        mouvements = self.obtenir_tous_mouvements(game.board, self.couleur)
        
        for depart, arrivee in mouvements:
            # Sauvegarder l'état actuel
            piece_capturee = game.board.obtenir_piece(arrivee)
            piece = game.board.obtenir_piece(depart)
            
            # Simuler le mouvement
            game.board.deplacer_piece(depart, arrivee)
            
            # Évaluer la nouvelle position
            score = self.evaluer_position(game.board)
            
            # Annuler le mouvement
            game.board.deplacer_piece(arrivee, depart)
            if piece_capturee:
                game.board.placer_piece(piece_capturee, arrivee)
            
            # Mettre à jour le meilleur mouvement
            if score > meilleur_score:
                meilleur_score = score
                meilleur_mouvement = (depart, arrivee)
        
        return meilleur_mouvement
