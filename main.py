# main.py
import pygame
from board import Board
from pieces import *
from gui import GUI

def main():
    # Création et lancement du jeu
    gui = GUI()
    gui.run()

if __name__ == "__main__":
    main()
    