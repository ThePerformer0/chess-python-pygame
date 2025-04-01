# main.py
import pygame
from board import Board
from pieces import *
from gui import GUI, MenuPrincipal

def main():
    pygame.init()
    
    # Afficher le menu principal
    menu = MenuPrincipal()
    mode_jeu = menu.run()
    
    # Lancer le jeu si un mode a été choisi
    if mode_jeu:
        gui = GUI(mode_jeu)
        gui.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()
    