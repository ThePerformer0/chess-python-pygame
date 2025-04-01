class ChessAI:
    def __init__(self, couleur):
        self.couleur = couleur
        
    def evaluer_position(self, board):
        # Attribuer des scores aux positions des pièces
        score = 0
        valeurs = {
            'pion': 1,
            'cavalier': 3,
            'fou': 3,
            'tour': 5,
            'reine': 9,
            'roi': 100
        }
        # Évaluation à implémenter
        return score
        
    def choisir_mouvement(self, board):
        # Implémenter l'algorithme Minimax ou similaire
        pass
