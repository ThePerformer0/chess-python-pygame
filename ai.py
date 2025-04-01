class ChessAI:
    def __init__(self, couleur):
        self.couleur = couleur
        self.profondeur_max = 3  # Profondeur de recherche
        self.valeurs_pieces = {
            'pion': 100,
            'cavalier': 320,
            'fou': 330,
            'tour': 500,
            'reine': 900,
            'roi': 20000
        }
        
        # Tables de position pour les pièces
        self.tables_position = {
            'pion': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5,  5, 10, 25, 25, 10,  5,  5],
                [0,  0,  0, 20, 20,  0,  0,  0],
                [5, -5,-10,  0,  0,-10, -5,  5],
                [5, 10, 10,-20,-20, 10, 10,  5],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],
            'cavalier': [
                [-50,-40,-30,-30,-30,-30,-40,-50],
                [-40,-20,  0,  0,  0,  0,-20,-40],
                [-30,  0, 10, 15, 15, 10,  0,-30],
                [-30,  5, 15, 20, 20, 15,  5,-30],
                [-30,  0, 15, 20, 20, 15,  0,-30],
                [-30,  5, 10, 15, 15, 10,  5,-30],
                [-40,-20,  0,  5,  5,  0,-20,-40],
                [-50,-40,-30,-30,-30,-30,-40,-50]
            ]
        }

    def evaluer_position(self, board):
        """Évaluation améliorée de la position"""
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board.obtenir_piece((i, j))
                if piece:
                    # Score de base des pièces
                    multiplicateur = 1 if piece.couleur == self.couleur else -1
                    score += self.valeurs_pieces[piece.type] * multiplicateur
                    
                    # Bonus de position
                    if piece.type in self.tables_position:
                        position_score = self.tables_position[piece.type][i][j]
                        if piece.couleur != 'blanc':
                            position_score = self.tables_position[piece.type][7-i][j]
                        score += position_score * multiplicateur
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

    def minimax(self, game, profondeur, alpha, beta, maximizing):
        """Algorithme Minimax avec élagage Alpha-Beta"""
        if profondeur == 0:
            return self.evaluer_position(game.board)

        if maximizing:
            meilleur_score = float('-inf')
            mouvements = self.obtenir_tous_mouvements(game.board, self.couleur)
            for depart, arrivee in mouvements:
                # Sauvegarder et simuler le mouvement
                piece_capturee = game.board.obtenir_piece(arrivee)
                game.board.deplacer_piece(depart, arrivee)
                
                score = self.minimax(game, profondeur - 1, alpha, beta, False)
                
                # Annuler le mouvement
                game.board.deplacer_piece(arrivee, depart)
                if piece_capturee:
                    game.board.placer_piece(piece_capturee, arrivee)
                
                meilleur_score = max(score, meilleur_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return meilleur_score
        else:
            meilleur_score = float('inf')
            couleur_adversaire = 'noir' if self.couleur == 'blanc' else 'blanc'
            mouvements = self.obtenir_tous_mouvements(game.board, couleur_adversaire)
            for depart, arrivee in mouvements:
                piece_capturee = game.board.obtenir_piece(arrivee)
                game.board.deplacer_piece(depart, arrivee)
                
                score = self.minimax(game, profondeur - 1, alpha, beta, True)
                
                game.board.deplacer_piece(arrivee, depart)
                if piece_capturee:
                    game.board.placer_piece(piece_capturee, arrivee)
                
                meilleur_score = min(score, meilleur_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return meilleur_score

    def choisir_mouvement(self, game):
        """Choisit le meilleur mouvement en utilisant Minimax"""
        meilleur_score = float('-inf')
        meilleur_mouvement = None
        alpha = float('-inf')
        beta = float('inf')
        
        mouvements = self.obtenir_tous_mouvements(game.board, self.couleur)
        
        for depart, arrivee in mouvements:
            piece_capturee = game.board.obtenir_piece(arrivee)
            game.board.deplacer_piece(depart, arrivee)
            
            score = self.minimax(game, self.profondeur_max - 1, alpha, beta, False)
            
            game.board.deplacer_piece(arrivee, depart)
            if piece_capturee:
                game.board.placer_piece(piece_capturee, arrivee)
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_mouvement = (depart, arrivee)
        
        return meilleur_mouvement
