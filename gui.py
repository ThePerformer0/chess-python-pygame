import pygame
from board import Board
from game import Game

class GUI:
    def __init__(self):
        self.TAILLE_CASE = 80
        self.LARGEUR = self.TAILLE_CASE * 8
        self.HAUTEUR = self.TAILLE_CASE * 8
        
        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))
        pygame.display.set_caption("Jeu d'Échecs")
        
        # Couleurs
        self.BLANC = (240, 217, 181)
        self.MARRON = (181, 136, 99)
        self.SURBRILLANCE = (186, 202, 68)
        self.ROUGE = (255, 0, 0)
        
        # Initialisation du jeu
        self.game = Game()
        self.charger_images()
        
        # Variables pour la sélection des pièces
        self.case_selectionnee = None
        self.mouvements_possibles = []
        
    def charger_images(self):
        """Charge les images des pièces depuis le dossier assets"""
        self.images = {}
        pieces = ['pion', 'tour', 'cavalier', 'fou', 'reine', 'roi']
        couleurs = ['blanc', 'noir']
        
        for piece in pieces:
            for couleur in couleurs:
                chemin = f"assets/{piece}_{couleur}.png"
                image = pygame.image.load(chemin)
                image = pygame.transform.scale(image, (self.TAILLE_CASE, self.TAILLE_CASE))
                self.images[f"{couleur}_{piece}"] = image
                
    def dessiner_plateau(self):
        """Dessine le plateau d'échecs"""
        for i in range(8):
            for j in range(8):
                couleur = self.BLANC if (i + j) % 2 == 0 else self.MARRON
                pygame.draw.rect(self.screen, couleur, 
                               (j * self.TAILLE_CASE, i * self.TAILLE_CASE, 
                                self.TAILLE_CASE, self.TAILLE_CASE))
                
    def dessiner_pieces(self):
        """Dessine les pièces sur le plateau"""
        for i in range(8):
            for j in range(8):
                piece = self.game.board.obtenir_piece((i, j))
                if piece:
                    image = self.images[f"{piece.couleur}_{piece.type}"]
                    self.screen.blit(image, 
                                   (j * self.TAILLE_CASE, i * self.TAILLE_CASE))
                    
    def dessiner_surbrillance(self):
        """Dessine la surbrillance pour la case sélectionnée et les mouvements possibles"""
        if self.case_selectionnee:
            i, j = self.case_selectionnee
            # Dessine un rectangle semi-transparent pour la case sélectionnée
            s = pygame.Surface((self.TAILLE_CASE, self.TAILLE_CASE))
            s.set_alpha(128)
            s.fill(self.SURBRILLANCE)
            self.screen.blit(s, (j * self.TAILLE_CASE, i * self.TAILLE_CASE))
            
            # Dessine les mouvements possibles
            for move in self.mouvements_possibles:
                i, j = move
                s = pygame.Surface((self.TAILLE_CASE, self.TAILLE_CASE))
                s.set_alpha(64)
                s.fill(self.SURBRILLANCE)
                self.screen.blit(s, (j * self.TAILLE_CASE, i * self.TAILLE_CASE))
                
    def obtenir_case_from_pixel(self, pos):
        """Convertit une position en pixels en coordonnées de case"""
        x, y = pos
        return (y // self.TAILLE_CASE, x // self.TAILLE_CASE)
    
    def gerer_clic(self, pos):
        """Gère les clics de souris"""
        case = self.obtenir_case_from_pixel(pos)
        
        if self.case_selectionnee is None:
            # Sélection d'une pièce
            if self.game.selectionner_piece(case):
                self.case_selectionnee = case
                piece = self.game.board.obtenir_piece(case)
                self.mouvements_possibles = piece.mouvements_valides(self.game.board.board)
        else:
            # Déplacement d'une pièce
            if case in self.mouvements_possibles:
                self.game.deplacer_piece(case)
            self.case_selectionnee = None
            self.mouvements_possibles = []
    
    def afficher_statut_partie(self):
        """Affiche le statut de la partie (échec, échec et mat)"""
        font = pygame.font.Font(None, 36)
        messages = []
        
        # Afficher le tour actuel
        joueur = "Blanc" if self.game.tour_blanc else "Noir"
        messages.append(f"Tour : {joueur}")
        
        # Afficher l'état d'échec
        if self.game.en_echec:
            messages.append("ÉCHEC!")
            
        # Afficher l'échec et mat
        if self.game.partie_terminee:
            messages.append("ÉCHEC ET MAT!")
            gagnant = "Blanc" if not self.game.tour_blanc else "Noir"
            messages.append(f"{gagnant} gagne!")
            
        # Afficher les messages
        y_offset = 10
        for message in messages:
            texte = font.render(message, True, self.ROUGE if "ÉCHEC" in message else (0, 0, 0))
            fond = pygame.Surface((texte.get_width() + 20, texte.get_height() + 10))
            fond.fill((255, 255, 255))
            fond.set_alpha(200)
            self.screen.blit(fond, (10, y_offset))
            self.screen.blit(texte, (20, y_offset + 5))
            y_offset += texte.get_height() + 15
            
    def run(self):
        """Boucle principale du jeu"""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.game.partie_terminee:  # Clic gauche
                        self.gerer_clic(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Touche R pour recommencer
                        self.game = Game()
            
            # Mise à jour de l'affichage
            self.dessiner_plateau()
            self.dessiner_surbrillance()
            self.dessiner_pieces()
            self.afficher_statut_partie()
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()

    def afficher_info_piece(self, case):
        """Affiche des informations sur la pièce survolée"""
        piece = self.game.board.obtenir_piece(case)
        if piece:
            font = pygame.font.Font(None, 24)
            info = f"{piece.couleur} {piece.type}"
            texte = font.render(info, True, (0, 0, 0))
            # Position de la souris
            mouse_pos = pygame.mouse.get_pos()
            # Créer un fond blanc pour le texte
            fond = pygame.Surface((texte.get_width() + 10, texte.get_height() + 10))
            fond.fill((255, 255, 255))
            fond.set_alpha(200)
            # Afficher le fond et le texte
            self.screen.blit(fond, (mouse_pos[0] + 10, mouse_pos[1] + 10))
            self.screen.blit(texte, (mouse_pos[0] + 15, mouse_pos[1] + 15))

    def afficher_tour_actuel(self):
        """Affiche le joueur actuel"""
        font = pygame.font.Font(None, 36)
        joueur = "Blanc" if self.game.tour_blanc else "Noir"
        texte = font.render(f"Tour : {joueur}", True, (0, 0, 0))
        # Créer un fond blanc pour le texte
        fond = pygame.Surface((texte.get_width() + 20, texte.get_height() + 10))
        fond.fill((255, 255, 255))
        fond.set_alpha(200)
        # Afficher le fond et le texte
        self.screen.blit(fond, (10, 10))
        self.screen.blit(texte, (20, 15))

    def afficher_menu_promotion(self):
        """Affiche le menu de promotion du pion"""
        options = ['reine', 'tour', 'fou', 'cavalier']
        couleur = 'blanc' if self.game.tour_blanc else 'noir'
        
        # Créer une surface pour le menu
        menu_surface = pygame.Surface((200, 300))
        menu_surface.fill((255, 255, 255))
        
        # Afficher les options
        for i, piece in enumerate(options):
            image = self.images[f"{couleur}_{piece}"]
            menu_surface.blit(image, (50, i * 75 + 10))
        
        # Afficher le menu au centre de l'écran
        pos_x = (self.LARGEUR - 200) // 2
        pos_y = (self.HAUTEUR - 300) // 2
        self.screen.blit(menu_surface, (pos_x, pos_y))
        pygame.display.flip()
        
        # Attendre le choix du joueur
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if pos_x <= mouse_pos[0] <= pos_x + 200:
                        index = (mouse_pos[1] - pos_y) // 75
                        if 0 <= index < len(options):
                            return options[index]