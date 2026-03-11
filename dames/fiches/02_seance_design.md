# Séance 2 — Design du plateau dans xTool CS (45 min)

## Objectifs

- Choisir le design de son jeu (couleurs, motifs)
- Découvrir xTool Creative Space
- Dessiner le damier-puzzle de son équipe

## Déroulement

### Choix de design par équipe (5 min)

Chaque équipe remplit sa fiche :
- 2 couleurs de PLA pour les pions
- Tissu pour la pochette (parmi les échantillons)
- Gravure sur le plateau : nom d'équipe, logo, date ?

```
Équipe : ______________  Membres : ___________________

Couleur pions A : ____________  B : ____________
Tissu pochette : _____________________________________
Gravure plateau : ____________________________________
```

### Découverte xTool Creative Space (5 min)

- Ouvrir xTool CS, présenter l'interface
- Les outils de base : rectangle, cercle, ligne, texte
- Les couleurs = les opérations :
  - Noir → GRAVURE (cases sombres)
  - Rouge → DÉCOUPE (contour + lignes de puzzle)

### Dessiner le damier (25 min)

**Étape 1 : le contour (3 min)**
1. Tracer un carré rouge de 160 × 160 mm (contour de découpe)

**Étape 2 : la grille (7 min)**
1. Tracer les 7 lignes horizontales rouges (espacement 20 mm)
2. Tracer les 7 lignes verticales rouges
3. Astuce : utiliser copier/coller + déplacement précis

**Étape 3 : les tenons puzzle (10 min)**
1. Sur chaque segment de grille, ajouter un tenon :
   - Dessiner un petit rectangle (~3 × 4 mm) à cheval sur la ligne
   - Coller un cercle (~3 mm de diamètre) au bout
   - Le tenon dépasse d'un côté de la ligne
2. Varier la position et le côté (haut/bas, gauche/droite)
   pour que les pièces s'emboîtent
3. Pas besoin que chaque tenon soit différent :
   l'important est que les pièces tiennent ensemble

**Étape 4 : les cases sombres (3 min)**
1. Remplir 1 case sur 2 en noir (32 carrés de 20 × 20 mm)
2. Astuce : faire une case, dupliquer en quinconce

**Étape 5 : personnalisation (2 min)**
1. Ajouter le nom d'équipe en noir (gravure) sous le damier

### Clôture (5 min) + réserve (5 min)

- Sauvegarder le projet xTool CS
- Vérifier : le carré fait bien 160 mm, les lignes sont rouges,
  les cases sont noires
- Prochaine fois : modélisation 3D du pion

## Conseils pour l'encadrant

- Montrer un exemple terminé au vidéoprojecteur
- Les tenons n'ont pas besoin d'être parfaits : des formes
  simples (rectangle + cercle) suffisent pour l'emboîtement
- Si une équipe est en avance, elle peut ajouter des motifs
  à graver sur les cases
- Un script Python (plateau/generate_puzzle.py) est disponible
  pour générer des plateaux de référence ou de secours

## Matériel

- 1 ordinateur par équipe (xTool CS installé)
- Vidéoprojecteur pour la démo
- Échantillons de PLA et tissu
- Fiches de design imprimées
- Optionnel : un plateau exemple découpé pour montrer le résultat
