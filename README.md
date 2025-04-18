# Jeu d'Échecs en Python

## Description
Un jeu d'échecs complet développé en Python avec Pygame, offrant la possibilité de jouer contre un autre joueur ou contre une IA. Le jeu implémente toutes les règles officielles des échecs, y compris les mouvements spéciaux comme le roque, la prise en passant et la promotion des pions.

![Menu Principal](assets/Menu-principal.PNG)

## Fonctionnalités
- Interface graphique complète avec menu principal
- Plusieurs modes de jeu :
  - Mode 2 joueurs
  - Mode contre l'IA (jouer les blancs ou les noirs)
- Règles complètes des échecs
- Aide intégrée et tutoriel
- Indication des mouvements possibles
- Détection des situations d'échec et mat

![Plateau de jeu](assets/plateau_de_jeu.PNG)

## Prérequis
- Python 3.x
- Pygame

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/ThePerformer0/chess-python-pygame.git
   cd jeu-echecs
   ```

2. Installez les dépendances :
   ```bash
   pip install pygame
   ```

3. Exécutez le jeu :
   ```bash
   python main.py
   ```

## Structure du projet

```
chess-python-pygame/
├── main.py       # Point d'entrée du programme
├── board.py      # Gestion du plateau de jeu
├── pieces.py     # Définition des pièces et leurs mouvements
├── gui.py        # Interface graphique
├── ai.py         # Intelligence artificielle
├── assets/       # Ressources graphiques
└── README.md     # Documentation
```

## Configuration des Images
Les images des pièces doivent être placées dans le dossier `assets/` avec la nomenclature suivante :
- `blanc_pion.png`
- `blanc_tour.png`
- `blanc_cavalier.png`
- `blanc_fou.png`
- `blanc_reine.png`
- `blanc_roi.png`
- `noir_pion.png`
- `noir_tour.png`
- `noir_cavalier.png`
- `noir_fou.png`
- `noir_reine.png`
- `noir_roi.png`

## Contrôles
- **Clic gauche** : Sélectionner et déplacer les pièces
- **Clic droit** : Annuler la sélection
- **Touche R** : Recommencer la partie
- **Touche Échap** : Retour au menu principal
- **Molette souris** : Faire défiler le menu d'aide

## Fonctionnalités de l'IA
L'IA utilise plusieurs stratégies avancées pour jouer :

### Algorithme Principal
- Utilisation de l'algorithme Minimax avec élagage Alpha-Beta
- Profondeur de recherche configurable (actuellement réglée à 3 coups d'avance)
- Optimisation des performances grâce à l'élagage des branches non prometteuses

### Système d'Évaluation des Positions
1. **Valeur des Pièces**
   - Pion : 100 points
   - Cavalier : 320 points
   - Fou : 330 points
   - Tour : 500 points
   - Reine : 900 points
   - Roi : 20000 points

2. **Tables de Position**
   - Bonus/Malus selon la position de chaque pièce sur l'échiquier
   - Évaluation spécifique pour les pions et les cavaliers
   - Adaptation des scores selon la couleur des pièces

3. **Évaluation Stratégique**
   - Analyse de la structure des pions
   - Contrôle du centre de l'échiquier
   - Sécurité du roi
   - Mobilité des pièces

### Optimisations
- Élagage Alpha-Beta pour réduire le nombre de positions analysées
- Gestion efficace de la mémoire
- Évaluation dynamique des positions

### Perspectives d'Amélioration
L'IA pourrait être encore améliorée avec :
- L'ajout de tables de position pour toutes les pièces
- L'implémentation d'une bibliothèque d'ouvertures
- L'augmentation de la profondeur de recherche
- L'ajout d'une table de transposition

## Règles Implémentées
- Mouvements standards de toutes les pièces
- Roque (petit et grand)
- Prise en passant
- Promotion des pions
- Détection de l'échec
- Détection de l'échec et mat

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Contact
- FEKE JIMMY - fekejimmy@gmail.com
- Lien du projet : https://github.com/ThePerformer0/chess-python-pygame