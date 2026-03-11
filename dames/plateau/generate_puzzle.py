#!/usr/bin/env python3
"""
Générateur SVG du damier-puzzle pour jeu de dames de voyage.
Découpe laser sur xTool M1 (contreplaqué 3mm).

Damier 8×8 découpé en 8×8 = 64 pièces puzzle (une pièce par case).
Chaque jonction jigsaw a une forme lisse (courbes de Bézier)
et une combinaison unique de paramètres, avec détection de collision
pour éviter que des tenons proches des coins se chevauchent.

Utilisation :
    # Générer 1 plateau :
    python3 generate_puzzle.py

    # Générer plusieurs plateaux pour différentes équipes :
    python3 generate_puzzle.py "Les Lions" "Les Tigres" "Équipe 3"

    # Générer N plateaux anonymes :
    python3 generate_puzzle.py --nombre 6

    # Découpe seule (sans gravure des cases noires) :
    python3 generate_puzzle.py --decoupe-seule
    python3 generate_puzzle.py --decoupe-seule "Les Lions" "Les Tigres"

Chaque équipe obtient un puzzle avec une combinaison unique de tenons.
Les fichiers SVG sont prêts à ouvrir dans Inkscape ou xTool Creative Space.
"""

import random
import os
import sys
from itertools import product

# === Paramètres du plateau ===
BOARD_MM = 160.0
N_CASES = 8
SQ_MM = BOARD_MM / N_CASES  # 20mm par case

# === Paramètres des tenons jigsaw ===
# Positions centrées : la plus excentrée (8mm) laisse au minimum
# 8 - 4.0 = 4mm entre le tenon le plus large et le coin.
TAB_POSITIONS = [8.0, 10.0, 12.0]
HEAD_HWS = [2.5, 3.2, 4.0]       # demi-largeur tête
DIRECTIONS = [1, -1]              # +1 bas/droite, -1 haut/gauche
NECK_HWS = [1.0, 1.5, 2.0]       # demi-largeur col (3 valeurs)
DEPTHS = [4.5, 5.5, 6.5]         # profondeur totale (3 valeurs)
# Total combinaisons : 3×3×2×3×3 = 162 ≥ 112 jonctions

# Marge minimale entre tenons (mm)
COLLISION_MARGIN = 0.8

# Distance minimale d'un tenon au coin de grille le plus proche (mm).
# Si les deux tenons perpendiculaires d'un coin sont plus proches que
# cette valeur, on considère qu'ils sont trop proches.
MIN_CORNER_GAP = 4.0

# === Paramètres SVG ===
SVG_MARGIN = 10.0
COLOR_CUT = "#FF0000"
COLOR_ENGRAVE = "#000000"
STROKE_W = 0.2

# === Toutes les combinaisons possibles ===
N_H_EDGES = (N_CASES - 1) * N_CASES   # 56
N_V_EDGES = N_CASES * (N_CASES - 1)   # 56
N_TOTAL = N_H_EDGES + N_V_EDGES       # 112

ALL_COMBOS = list(product(
    range(len(TAB_POSITIONS)),
    range(len(HEAD_HWS)),
    range(len(DIRECTIONS)),
    range(len(NECK_HWS)),
    range(len(DEPTHS)),
))
assert len(ALL_COMBOS) >= N_TOTAL, (
    f"{len(ALL_COMBOS)} combinaisons < {N_TOTAL} jonctions")


def get_params(combo):
    """Convertit les indices en valeurs physiques."""
    pos_i, hw_i, dir_i, nw_i, d_i = combo
    return (TAB_POSITIONS[pos_i], HEAD_HWS[hw_i],
            DIRECTIONS[dir_i], NECK_HWS[nw_i], DEPTHS[d_i])


# =============================================================
#  Détection de collision entre tenons
# =============================================================

def bbox_h(cr, col, combo):
    """Boîte englobante d'un tenon horizontal en coordonnées plateau."""
    pos, hw, direction, nw, depth = get_params(combo)
    cx = col * SQ_MM + pos
    ey = (cr + 1) * SQ_MM
    dy = depth * direction
    return (cx - hw, min(ey, ey + dy), cx + hw, max(ey, ey + dy))


def bbox_v(row, cc, combo):
    """Boîte englobante d'un tenon vertical en coordonnées plateau."""
    pos, hw, direction, nw, depth = get_params(combo)
    cy = row * SQ_MM + pos
    ex = (cc + 1) * SQ_MM
    dx = depth * direction
    return (min(ex, ex + dx), cy - hw, max(ex, ex + dx), cy + hw)


def overlaps(b1, b2):
    """Vérifie si deux boîtes englobantes se chevauchent (avec marge)."""
    m = COLLISION_MARGIN
    return (b1[0] - m < b2[2] and b1[2] + m > b2[0] and
            b1[1] - m < b2[3] and b1[3] + m > b2[1])


def corner_conflict(h_key, h_combo, v_key, v_combo):
    """Vérifie si un tenon h et un tenon v sont tous deux trop proches
    d'un coin de grille partagé.

    Au coin, on mesure :
      h_gap = distance entre le bord du tenon h et le coin (en x)
      v_gap = distance entre le bord du tenon v et le coin (en y)
    Si les deux gaps sont < MIN_CORNER_GAP → conflit.
    """
    cr, col = h_key
    row, cc = v_key
    pos_h, hw_h, _, _, _ = get_params(h_combo)
    pos_v, hw_v, _, _, _ = get_params(v_combo)

    # Le coin partagé est à x=(cc+1)*SQ, y=(cr+1)*SQ.
    # h-edge couvre la colonne col : x de col*SQ à (col+1)*SQ
    # v-edge couvre la ligne row  : y de row*SQ à (row+1)*SQ
    # Pour qu'ils partagent un coin :
    #   cc = col-1 (coin gauche) ou cc = col (coin droit)
    #   cr = row-1 (coin haut)   ou cr = row (coin bas)

    if cc == col - 1:
        h_gap = pos_h - hw_h          # bord gauche du tenon h au coin
    elif cc == col:
        h_gap = SQ_MM - pos_h - hw_h  # bord droit du tenon h au coin
    else:
        return False

    if cr == row - 1:
        v_gap = pos_v - hw_v          # bord haut du tenon v au coin
    elif cr == row:
        v_gap = SQ_MM - pos_v - hw_v  # bord bas du tenon v au coin
    else:
        return False

    return h_gap < MIN_CORNER_GAP and v_gap < MIN_CORNER_GAP


def h_neighbor_v_keys(cr, col):
    """Clés des arêtes verticales voisines d'une arête horizontale."""
    neighbors = []
    for row in [cr, cr + 1]:
        if 0 <= row < N_CASES:
            if col > 0:
                neighbors.append((row, col - 1))
            if col < N_CASES - 1:
                neighbors.append((row, col))
    return neighbors


def v_neighbor_h_keys(row, cc):
    """Clés des arêtes horizontales voisines d'une arête verticale."""
    neighbors = []
    for cr in [row - 1, row]:
        if 0 <= cr < N_CASES - 1:
            if cc >= 0:
                neighbors.append((cr, cc))
            if cc + 1 < N_CASES:
                neighbors.append((cr, cc + 1))
    return neighbors


# =============================================================
#  Assignation greedy avec évitement de collision
# =============================================================

def assign_combos(seed=42):
    """Assigne des combinaisons uniques sans collision entre tenons voisins."""
    random.seed(seed)
    combos = list(ALL_COMBOS)
    random.shuffle(combos)

    h_edges = {}
    v_edges = {}
    used = set()

    # 1) Assigner les arêtes horizontales
    for cr in range(N_CASES - 1):
        for col in range(N_CASES):
            assigned = False
            for combo in combos:
                if combo in used:
                    continue
                bb = bbox_h(cr, col, combo)
                conflict = False
                for vk in h_neighbor_v_keys(cr, col):
                    if vk in v_edges:
                        vb = bbox_v(vk[0], vk[1], v_edges[vk])
                        if overlaps(bb, vb):
                            conflict = True
                            break
                        if corner_conflict((cr, col), combo, vk, v_edges[vk]):
                            conflict = True
                            break
                if not conflict:
                    h_edges[(cr, col)] = combo
                    used.add(combo)
                    assigned = True
                    break
            if not assigned:
                raise RuntimeError(
                    f"Impossible d'assigner h_edge ({cr},{col}) sans collision")

    # 2) Assigner les arêtes verticales
    for row in range(N_CASES):
        for cc in range(N_CASES - 1):
            assigned = False
            for combo in combos:
                if combo in used:
                    continue
                bb = bbox_v(row, cc, combo)
                conflict = False
                # Vérifier contre les h-edges voisins
                for hk in v_neighbor_h_keys(row, cc):
                    if hk in h_edges:
                        hb = bbox_h(hk[0], hk[1], h_edges[hk])
                        if overlaps(bb, hb):
                            conflict = True
                            break
                        if corner_conflict(hk, h_edges[hk], (row, cc), combo):
                            conflict = True
                            break
                # Vérifier aussi contre les v-edges déjà assignés (voisins)
                if not conflict:
                    for dr in [-1, 0, 1]:
                        nr = row + dr
                        for dc in [-1, 0, 1]:
                            nc = cc + dc
                            if (nr, nc) in v_edges and (nr, nc) != (row, cc):
                                if overlaps(bb, bbox_v(nr, nc, v_edges[(nr, nc)])):
                                    conflict = True
                                    break
                        if conflict:
                            break
                if not conflict:
                    v_edges[(row, cc)] = combo
                    used.add(combo)
                    assigned = True
                    break
            if not assigned:
                raise RuntimeError(
                    f"Impossible d'assigner v_edge ({row},{cc}) sans collision")

    return h_edges, v_edges


def verify(h_edges, v_edges):
    """Vérifie l'unicité des combinaisons et l'absence de collision."""
    # Unicité
    all_used = list(h_edges.values()) + list(v_edges.values())
    assert len(set(all_used)) == len(all_used), "Doublons détectés !"

    # Collisions h vs v (chevauchement + proximité coin)
    collisions = []
    for hk, hc in h_edges.items():
        hb = bbox_h(hk[0], hk[1], hc)
        for vk in h_neighbor_v_keys(hk[0], hk[1]):
            if vk in v_edges:
                vc = v_edges[vk]
                vb = bbox_v(vk[0], vk[1], vc)
                if overlaps(hb, vb):
                    collisions.append(("chevauchement", hk, vk))
                elif corner_conflict(hk, hc, vk, vc):
                    collisions.append(("coin_proche", hk, vk))

    return collisions


# =============================================================
#  Génération SVG
# =============================================================

def f(v):
    return f"{v:.3f}"


def tab_h(x_start, y, combo):
    """Tenon lisse sur arête horizontale (Bézier cubiques)."""
    pos, hw, direction, nw, depth = get_params(combo)
    cx = x_start + pos
    dy = depth * direction
    t1, t2, t3 = 0.20, 0.50, 0.75

    p = f"L {f(cx - nw)},{f(y)} "
    p += f"L {f(cx - nw)},{f(y + dy * t1)} "
    p += (f"C {f(cx - nw)},{f(y + dy * t2)} "
          f"{f(cx - hw)},{f(y + dy * t2)} "
          f"{f(cx - hw)},{f(y + dy * t3)} ")
    p += (f"C {f(cx - hw)},{f(y + dy)} "
          f"{f(cx + hw)},{f(y + dy)} "
          f"{f(cx + hw)},{f(y + dy * t3)} ")
    p += (f"C {f(cx + hw)},{f(y + dy * t2)} "
          f"{f(cx + nw)},{f(y + dy * t2)} "
          f"{f(cx + nw)},{f(y + dy * t1)} ")
    p += f"L {f(cx + nw)},{f(y)} "
    return p


def tab_v(x, y_start, combo):
    """Tenon lisse sur arête verticale (Bézier cubiques)."""
    pos, hw, direction, nw, depth = get_params(combo)
    cy = y_start + pos
    dx = depth * direction
    t1, t2, t3 = 0.20, 0.50, 0.75

    p = f"L {f(x)},{f(cy - nw)} "
    p += f"L {f(x + dx * t1)},{f(cy - nw)} "
    p += (f"C {f(x + dx * t2)},{f(cy - nw)} "
          f"{f(x + dx * t2)},{f(cy - hw)} "
          f"{f(x + dx * t3)},{f(cy - hw)} ")
    p += (f"C {f(x + dx)},{f(cy - hw)} "
          f"{f(x + dx)},{f(cy + hw)} "
          f"{f(x + dx * t3)},{f(cy + hw)} ")
    p += (f"C {f(x + dx * t2)},{f(cy + hw)} "
          f"{f(x + dx * t2)},{f(cy + nw)} "
          f"{f(x + dx * t1)},{f(cy + nw)} ")
    p += f"L {f(x)},{f(cy + nw)} "
    return p


def engrave_squares():
    rects = []
    for row in range(N_CASES):
        for col in range(N_CASES):
            if (row + col) % 2 == 1:
                x = SVG_MARGIN + col * SQ_MM
                y = SVG_MARGIN + row * SQ_MM
                rects.append(
                    f'    <rect x="{f(x)}" y="{f(y)}" '
                    f'width="{f(SQ_MM)}" height="{f(SQ_MM)}" '
                    f'fill="{COLOR_ENGRAVE}" stroke="none"/>')
    return "\n".join(rects)


def outer_border():
    x0, y0 = SVG_MARGIN, SVG_MARGIN
    x1, y1 = SVG_MARGIN + BOARD_MM, SVG_MARGIN + BOARD_MM
    d = (f"M {f(x0)},{f(y0)} L {f(x1)},{f(y0)} "
         f"L {f(x1)},{f(y1)} L {f(x0)},{f(y1)} Z")
    return (f'    <path d="{d}" '
            f'fill="none" stroke="{COLOR_CUT}" stroke-width="{f(STROKE_W)}"/>')


def horizontal_cuts(h_edges):
    paths = []
    for cr in range(N_CASES - 1):
        y = SVG_MARGIN + (cr + 1) * SQ_MM
        d = f"M {f(SVG_MARGIN)},{f(y)} "
        for col in range(N_CASES):
            x_start = SVG_MARGIN + col * SQ_MM
            x_end = x_start + SQ_MM
            d += tab_h(x_start, y, h_edges[(cr, col)])
            d += f"L {f(x_end)},{f(y)} "
        paths.append(
            f'    <path d="{d}" '
            f'fill="none" stroke="{COLOR_CUT}" stroke-width="{f(STROKE_W)}"/>')
    return "\n".join(paths)


def vertical_cuts(v_edges):
    paths = []
    for cc in range(N_CASES - 1):
        x = SVG_MARGIN + (cc + 1) * SQ_MM
        d = f"M {f(x)},{f(SVG_MARGIN)} "
        for row in range(N_CASES):
            y_start = SVG_MARGIN + row * SQ_MM
            y_end = y_start + SQ_MM
            d += tab_v(x, y_start, v_edges[(row, cc)])
            d += f"L {f(x)},{f(y_end)} "
        paths.append(
            f'    <path d="{d}" '
            f'fill="none" stroke="{COLOR_CUT}" stroke-width="{f(STROKE_W)}"/>')
    return "\n".join(paths)


def label_text(text):
    """Texte gravé sous le plateau (nom d'équipe, etc.)."""
    if not text:
        return ""
    x = SVG_MARGIN + BOARD_MM / 2
    y = SVG_MARGIN + BOARD_MM + 7
    return (f'    <text x="{f(x)}" y="{f(y)}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="5" '
            f'fill="{COLOR_ENGRAVE}">{text}</text>')


def generate_svg(h_edges, v_edges, team_name="", engrave=True):
    w = BOARD_MM + 2 * SVG_MARGIN
    h = BOARD_MM + 2 * SVG_MARGIN + (10 if team_name else 0)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg"',
        f'     width="{f(w)}mm" height="{f(h)}mm"',
        f'     viewBox="0 0 {f(w)} {f(h)}">',
    ]

    if engrave:
        parts += [
            '',
            '  <!-- Cases sombres (gravure laser) -->',
            '  <g id="engrave">',
            engrave_squares(),
        ]
        lbl = label_text(team_name)
        if lbl:
            parts.append(lbl)
        parts.append('  </g>')

    parts += [
        '',
        '  <!-- Lignes de découpe (laser) -->',
        '  <g id="cut">',
        outer_border(),
        horizontal_cuts(h_edges),
        vertical_cuts(v_edges),
        '  </g>',
        '',
        '</svg>',
    ]
    return "\n".join(parts)


# =============================================================
#  Point d'entrée
# =============================================================

def sanitize_filename(name):
    """Transforme un nom d'équipe en nom de fichier valide."""
    safe = name.lower().replace(" ", "_")
    return "".join(c for c in safe if c.isalnum() or c == "_")


def generate_one(seed, team_name, out_dir, engrave=True):
    """Génère un SVG pour une équipe donnée."""
    h_edges, v_edges = assign_combos(seed=seed)
    collisions = verify(h_edges, v_edges)
    n_unique = len(set(list(h_edges.values()) + list(v_edges.values())))
    print(f"  Combinaisons uniques : {n_unique}/{N_TOTAL}")
    print(f"  Collisions           : {len(collisions)}")
    if collisions:
        for item in collisions:
            print(f"    {item[0]}: h{item[1]} vs v{item[2]}")

    svg = generate_svg(h_edges, v_edges, team_name=team_name, engrave=engrave)
    if team_name:
        filename = f"damier_{sanitize_filename(team_name)}.svg"
    else:
        filename = f"damier_{seed}.svg"
    out_path = os.path.join(out_dir, filename)
    with open(out_path, "w") as fh:
        fh.write(svg)
    print(f"  → {out_path}")
    return out_path


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # Parser les arguments
    args = sys.argv[1:]
    teams = []
    engrave = True

    # Extraire l'option --decoupe-seule
    if "--decoupe-seule" in args:
        engrave = False
        args.remove("--decoupe-seule")

    if not args:
        # Aucun argument : 1 plateau anonyme
        teams = [("", 42)]
    elif args[0] == "--nombre":
        # --nombre N : N plateaux anonymes
        n = int(args[1]) if len(args) > 1 else 1
        teams = [(f"Équipe {i+1}", 42 + i) for i in range(n)]
    else:
        # Noms d'équipes en arguments positionnels
        teams = [(name, 42 + i) for i, name in enumerate(args)]

    mode = "découpe seule" if not engrave else "gravure + découpe"
    print(f"Génération de {len(teams)} plateau(x) ({mode})…")
    print(f"Plateau : {BOARD_MM:.0f}×{BOARD_MM:.0f}mm, "
          f"{N_CASES}×{N_CASES} = {N_CASES**2} pièces")
    print(f"Jonctions : {N_TOTAL}, marge anti-collision : {COLLISION_MARGIN}mm\n")

    for team_name, seed in teams:
        label = team_name if team_name else f"seed={seed}"
        print(f"[{label}]")
        generate_one(seed, team_name, out_dir, engrave=engrave)
        print()
