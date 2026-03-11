# Séance 5 — Impression 3D des pions (45 min)

## Objectifs

- Comprendre le principe de l'impression FDM
- Préparer son fichier dans Cura (slicer)
- Exporter le G-code prêt à imprimer

Les impressions sont lancées par l'encadrant hors séances
(~1h par couleur). Les élèves récupèrent leurs pions à la
séance suivante.

## Déroulement

### Principe de l'impression 3D (10 min)

- Le PLA est fondu (200 degrés) et déposé couche par couche
- Montrer sur l'Ultimaker : bobine, buse (ne pas toucher !),
  plateau chauffant
- Montrer un pion déjà imprimé : observer les couches
- Slicer = logiciel qui transforme un volume 3D en instructions
  pour la machine (G-code)
- Vocabulaire : couche, remplissage, brim, buse, rétraction

### Préparation dans Cura (25 min)

**Exercice guidé :**
1. Ouvrir Cura, sélectionner le profil Ultimaker 2+
2. Importer le STL du pion de l'équipe
3. Vérifier les dimensions (15 mm de diamètre)
4. Appliquer les réglages :

| Paramètre           | Valeur    |
|----------------------|-----------|
| Hauteur de couche    | 0.2 mm    |
| Remplissage          | 20%       |
| Vitesse              | 50 mm/s   |
| Température buse     | 205 °C    |
| Température plateau  | 60 °C     |
| Support              | Non       |
| Adhérence            | Brim 5 mm |

5. Disposer 12 pions + 3-4 dames sur le plateau virtuel
   (espacement ~5 mm entre chaque pièce)
6. Observer :
   - Le temps estimé (en bas à droite)
   - La quantité de PLA utilisée
   - La vue en couches (bouton « Preview »)
7. Exporter le G-code sur carte SD (1 fichier par couleur)

**Questions pour les élèves :**
- Que se passe-t-il si on augmente le remplissage à 100% ?
  (plus lourd, plus long, plus solide)
- Pourquoi mettre un brim ? (meilleure adhérence au plateau)
- Pourquoi pas de support ? (le pion a une base plate)

### Dépannage : que faire si… (5 min)

| Problème             | Solution dans Cura            |
|----------------------|-------------------------------|
| Temps trop long      | Réduire remplissage à 15%     |
| Pion trop grand      | Échelle 95%                   |
| Fils entre pions     | Activer rétraction            |

### Clôture (5 min)

- Remettre les cartes SD à l'encadrant
- Les impressions seront lancées avant la prochaine séance
- Récupération des pions en début de séance 6
- Conseil : prévoir 1-2 pions de réserve par couleur

## Note pour l'encadrant

**Impressions à lancer hors séance :**
- Prévoir ~1h par plateau (12 pions + dames)
- 2 Ultimaker = 2 couleurs en parallèle
- Vérifier l'adhérence des premières couches
- Après impression : retirer le brim à la pince coupante
- Stocker les pions par équipe dans des sachets étiquetés

## Matériel

- 1 ordinateur par équipe (Cura installé)
- Fichiers STL de chaque équipe
- Cartes SD
- 1 pion déjà imprimé à montrer
- Vidéoprojecteur pour la démo
