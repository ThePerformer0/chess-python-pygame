import pygame
import time
from board import Board
from game import Game

class MenuPrincipal:
    def __init__(self):
        self.LARGEUR_MIN = 800
        self.HAUTEUR_MIN = 640
        self.screen = pygame.display.set_mode((self.LARGEUR_MIN, self.HAUTEUR_MIN), pygame.RESIZABLE)
        pygame.display.set_caption("Échecs - Menu Principal")
        
        # Couleurs
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS = (128, 128, 128)
        self.BLEU = (0, 100, 255)
        
        # Police
        self.font_titre = pygame.font.Font(None, 74)
        self.font_bouton = pygame.font.Font(None, 50)
        self.font_texte = pygame.font.Font(None, 36)
        
    def dessiner_bouton(self, texte, position, survol=False):
        """Dessine un bouton avec effet de survol"""
        couleur = self.BLEU if survol else self.GRIS
        texte_surface = self.font_bouton.render(texte, True, self.BLANC)
        rect = pygame.Rect(position[0], position[1], 300, 60)
        pygame.draw.rect(self.screen, couleur, rect, border_radius=10)
        
        # Centrer le texte dans le bouton
        text_rect = texte_surface.get_rect(center=rect.center)
        self.screen.blit(texte_surface, text_rect)
        
        return rect
        
    def afficher_aide(self):
        """Affiche la page d'aide avec les instructions du jeu"""
        running = True
        scroll_y = 0  # Position de défilement
        scroll_speed = 30  # Vitesse de défilement
        
        # Instructions complètes
        instructions = [
            "Contrôles du jeu :",
            "",
            "• Clic gauche : Sélectionner et déplacer les pièces",
            "• Clic droit : Annuler la sélection",
            "• Touche R : Recommencer la partie",
            "• Touche Échap : Retour au menu principal",
            "",
            "Règles spéciales :",
            "",
            "• Le roque est possible si le roi et la tour n'ont pas bougé",
            "• La prise en passant est disponible pour les pions",
            "• Les pions peuvent être promus en atteignant la dernière rangée",
            "",
            "État du jeu :",
            "",
            "• Le joueur actif est affiché en haut à gauche",
            "• Les situations d'échec et mat sont indiquées",
            "• Les mouvements possibles sont surlignés en vert",
            "",
            "Modes de jeu :",
            "",
            "• 2 Joueurs : Jouez contre un autre joueur en local",
            "• IA - Jouer Blanc : Vous jouez les blancs contre l'IA",
            "• IA - Jouer Noir : Vous jouez les noirs contre l'IA"
        ]
        
        # Calculer la hauteur totale du contenu
        ligne_hauteur = 30
        contenu_hauteur = len(instructions) * ligne_hauteur
        
        while running:
            # Obtenir les dimensions actuelles de la fenêtre
            largeur_actuelle = self.screen.get_width()
            hauteur_actuelle = self.screen.get_height()
            
            # Zone visible maximale pour le contenu
            zone_visible_hauteur = hauteur_actuelle - 200  # Espace pour titre et bouton retour
            
            # Limiter le défilement
            scroll_y = max(min(scroll_y, 0), -contenu_hauteur + zone_visible_hauteur)
            
            self.screen.fill(self.BLANC)
            
            # Créer une surface pour le contenu défilant
            contenu_surface = pygame.Surface((largeur_actuelle - 100, contenu_hauteur))
            contenu_surface.fill(self.BLANC)
            
            # Dessiner le texte sur la surface de contenu
            y_offset = 0
            for ligne in instructions:
                texte = self.font_texte.render(ligne, True, self.NOIR)
                contenu_surface.blit(texte, (0, y_offset))
                y_offset += ligne_hauteur
            
            # Dessiner la surface de contenu avec le défilement
            self.screen.blit(contenu_surface, (50, 120 + scroll_y))
            
            # Dessiner des indicateurs de défilement si nécessaire
            if contenu_hauteur > zone_visible_hauteur:
                if scroll_y < 0:  # Plus de contenu en bas
                    pygame.draw.polygon(self.screen, self.NOIR, [
                        (largeur_actuelle//2 - 10, hauteur_actuelle - 60),
                        (largeur_actuelle//2 + 10, hauteur_actuelle - 60),
                        (largeur_actuelle//2, hauteur_actuelle - 40)
                    ])
                if scroll_y > -contenu_hauteur + zone_visible_hauteur:  # Plus de contenu en haut
                    pygame.draw.polygon(self.screen, self.NOIR, [
                        (largeur_actuelle//2 - 10, 100),
                        (largeur_actuelle//2 + 10, 100),
                        (largeur_actuelle//2, 80)
                    ])
            
            # Bouton retour (fixe en bas)
            mouse_pos = pygame.mouse.get_pos()
            retour_pos = (50, hauteur_actuelle - 550)
            rect_retour = self.dessiner_bouton("Retour", retour_pos,
                pygame.Rect(retour_pos[0], retour_pos[1], 300, 60).collidepoint(mouse_pos))
            
            pygame.display.flip()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.VIDEORESIZE:
                    nouvelle_largeur = max(event.w, self.LARGEUR_MIN)
                    nouvelle_hauteur = max(event.h, self.HAUTEUR_MIN)
                    self.screen = pygame.display.set_mode((nouvelle_largeur, nouvelle_hauteur), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and rect_retour.collidepoint(mouse_pos):
                        return
                    elif event.button == 4:  # Molette vers le haut
                        scroll_y += scroll_speed
                    elif event.button == 5:  # Molette vers le bas
                        scroll_y -= scroll_speed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_UP:
                        scroll_y += scroll_speed
                    elif event.key == pygame.K_DOWN:
                        scroll_y -= scroll_speed

    def run(self):
        """Affiche le menu principal et retourne le mode de jeu choisi"""
        running = True
        mode_choisi = None
        
        while running:
            # Obtenir les dimensions actuelles de la fenêtre
            largeur_actuelle = self.screen.get_width()
            hauteur_actuelle = self.screen.get_height()
            
            # Position de la souris
            mouse_pos = pygame.mouse.get_pos()
            
            # Dessiner le fond
            self.screen.fill(self.BLANC)
            
            # Dessiner le titre centré
            titre = self.font_titre.render("Jeu d'Échecs", True, self.NOIR)
            titre_rect = titre.get_rect(center=(largeur_actuelle//2, 100))
            self.screen.blit(titre, titre_rect)
            
            # Calculer les positions des boutons en fonction de la taille de la fenêtre
            centre_x = largeur_actuelle // 2 - 150  # 150 est la moitié de la largeur du bouton
            
            # Positions des boutons
            bouton_2joueurs_pos = (centre_x, hauteur_actuelle * 0.3)
            bouton_ia_blanc_pos = (centre_x, hauteur_actuelle * 0.4)
            bouton_ia_noir_pos = (centre_x, hauteur_actuelle * 0.5)
            bouton_aide_pos = (centre_x, hauteur_actuelle * 0.6)
            
            # Dessiner les boutons avec effet de survol
            rect_2joueurs = self.dessiner_bouton("2 Joueurs", bouton_2joueurs_pos, 
                pygame.Rect(bouton_2joueurs_pos[0], bouton_2joueurs_pos[1], 300, 60).collidepoint(mouse_pos))
            
            rect_ia_blanc = self.dessiner_bouton("IA VS Jouer Blanc", bouton_ia_blanc_pos,
                pygame.Rect(bouton_ia_blanc_pos[0], bouton_ia_blanc_pos[1], 300, 60).collidepoint(mouse_pos))
            
            rect_ia_noir = self.dessiner_bouton("IA VS Jouer Noir", bouton_ia_noir_pos,
                pygame.Rect(bouton_ia_noir_pos[0], bouton_ia_noir_pos[1], 300, 60).collidepoint(mouse_pos))
            
            rect_aide = self.dessiner_bouton("Comment Jouer", bouton_aide_pos,
                pygame.Rect(bouton_aide_pos[0], bouton_aide_pos[1], 300, 60).collidepoint(mouse_pos))
            
            pygame.display.flip()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.VIDEORESIZE:
                    # Mettre à jour la taille de la fenêtre avec une taille minimale
                    nouvelle_largeur = max(event.w, self.LARGEUR_MIN)
                    nouvelle_hauteur = max(event.h, self.HAUTEUR_MIN)
                    self.screen = pygame.display.set_mode((nouvelle_largeur, nouvelle_hauteur), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        if rect_2joueurs.collidepoint(mouse_pos):
                            return "2joueurs"
                        elif rect_ia_blanc.collidepoint(mouse_pos):
                            return "ia_noir"
                        elif rect_ia_noir.collidepoint(mouse_pos):
                            return "ia_blanc"
                        elif rect_aide.collidepoint(mouse_pos):
                            self.afficher_aide()
                            
        return None

class GUI:
    def __init__(self, mode_jeu):
        self.TAILLE_CASE = 80
        self.LARGEUR = self.TAILLE_CASE * 8
        self.HAUTEUR = self.TAILLE_CASE * 8
        
        # Redimensionner la fenêtre pour le jeu
        self.screen = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))
        pygame.display.set_caption("Jeu d'Échecs")
        
        # Couleurs
        self.BLANC = (240, 217, 181)
        self.MARRON = (181, 136, 99)
        self.SURBRILLANCE = (186, 202, 68)
        self.ROUGE = (255, 0, 0)
        
        # Initialisation du jeu
        self.game = Game(mode_jeu)
        self.charger_images()
        
        # Variables pour la sélection des pièces
        self.case_selectionnee = None
        self.mouvements_possibles = []
        
        # Délai pour les mouvements de l'IA (en secondes)
        self.DELAI_IA = 1.0
        
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
        running = True
        clock = pygame.time.Clock()
        dernier_mouvement_ia = 0
        
        while running:
            temps_actuel = time.time()
            
            # Faire jouer l'IA si c'est son tour et si assez de temps s'est écoulé
            if (not self.game.partie_terminee and 
                temps_actuel - dernier_mouvement_ia >= self.DELAI_IA):
                if self.game.jouer_tour_ia():
                    dernier_mouvement_ia = temps_actuel
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.game.partie_terminee:
                        if not (self.game.ia and 
                               ((self.game.tour_blanc and self.game.ia.couleur == 'blanc') or 
                                (not self.game.tour_blanc and self.game.ia.couleur == 'noir'))):
                            self.gerer_clic(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Touche R pour recommencer
                        self.game = Game(self.game.mode_jeu)
                        dernier_mouvement_ia = 0
            
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