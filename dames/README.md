# Jeu de Dames de Voyage

Projet FabLab pour collégiens : concevoir et fabriquer un jeu de dames de voyage complet en utilisant trois techniques de fabrication numérique.

## Le produit fini

| Composant | Machine | Technique |
|-----------|---------|-----------|
| Plateau puzzle 8×8 (64 pièces, contreplaqué 3mm) | xTool M1 | Découpe & gravure laser |
| Pions 12+12 et dames (PLA) | Ultimaker 2+ | Impression 3D FDM |
| Pochette à cordon avec poche et appliqué | Machine à coudre | Couture |

## Structure du projet

```
dames/
├── fiches/                  # Fiches pédagogiques (8 séances de 45 min)
│   ├── 00_projet_overview.md
│   ├── 01_seance_decouverte.md
│   ├── 02_seance_design.md
│   ├── 03_seance_tinkercad.md
│   ├── 04_seance_laser.md
│   ├── 05_seance_impression3d.md
│   ├── 06_seance_couture1.md
│   ├── 07_seance_couture2.md
│   └── 08_seance_finale.md
├── plateau/                 # Damier-puzzle
│   ├── generate_puzzle.py       # Générateur SVG (outil encadrant)
│   └── damier_puzzle.svg        # Exemple généré
├── pions/                   # Pions et dames
│   ├── generate_pions.py        # Générateur STL
│   ├── pion.stl                 # Pion Ø15×5mm
│   └── dame.stl                 # Dame Ø15×8mm avec rainure
└── pochette/                # Patron de couture
    ├── generate_pochette.py     # Générateur SVG du patron
    └── pochette_patron.svg      # Patron généré
```

## Déroulement pédagogique

| Séance | Thème | Logiciel |
|--------|-------|----------|
| 1 | Découverte FabLab, projet, règles du jeu | — |
| 2 | Design du plateau (grille + tenons) | xTool Creative Space |
| 3 | Modélisation 3D des pions | Tinkercad |
| 4 | Découpe laser du plateau | xTool Creative Space |
| 5 | Préparation impression 3D | Cura |
| 6 | Couture pochette — découpe et début | Machine à coudre |
| 7 | Couture pochette — assemblage | Machine à coudre |
| 8 | Assemblage final, test et présentation | — |

Les élèves conçoivent leur plateau eux-mêmes dans xTool Creative Space avec des tenons simples (rectangle + cercle). Les impressions 3D sont lancées par l'encadrant entre les séances.

## Scripts (outils encadrant)

Les scripts Python sont des outils pour l'encadrant, pas pour les élèves.

### Plateau puzzle

```bash
# Générer 1 plateau
python3 plateau/generate_puzzle.py

# Générer des plateaux pour des équipes nommées
python3 plateau/generate_puzzle.py "Les Lions" "Les Tigres" "Équipe 3"

# Générer N plateaux numérotés
python3 plateau/generate_puzzle.py --nombre 6
```

Chaque plateau a une combinaison unique de tenons (courbes de Bézier) avec détection de collision automatique.

### Pions

```bash
python3 pions/generate_pions.py
# → pion.stl (Ø15×5mm) + dame.stl (Ø15×8mm)
```

### Patron pochette

```bash
python3 pochette/generate_pochette.py
# → pochette_patron.svg (corps ×2, poche, appliqué feutrine)
```

## Matériel par jeu

- Contreplaqué 3mm : 1 plaque 20×20 cm
- PLA 2 couleurs : ~10g chacun
- Tissu coton/lin : ~50×70 cm
- Feutrine : chute 8×8 cm
- Cordon : ~60 cm
- Fil à coudre

## Prérequis

- Python 3 (aucune dépendance externe)
- xTool Creative Space
- Cura
- Tinkercad (navigateur web)

## Licence

Voir [LICENSE](../LICENSE) à la racine du dépôt.
