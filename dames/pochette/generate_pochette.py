#!/usr/bin/env python3
"""
Générateur SVG du patron de la pochette pour jeu de dames de voyage.
Découpe laser sur xTool M1 (tissu coton ou lin).

La pochette est un sac à cordon contenant :
  - 64 pièces de puzzle (20×20×3mm chacune)
  - 24+ pions (diam 15mm, hauteur 5-8mm)

Pièces du patron :
  1. Corps du sac (×2) : rectangles avec repères de couture
  2. Séparateur intérieur (×1) : poche pour les pions
  3. Appliqué décoratif (×1) : motif damier en feutrine

Utilisation :
    python3 generate_pochette.py
    → génère pochette_patron.svg dans le même répertoire
"""

import os

# === Dimensions finies du sac (mm) ===
SAC_LARGEUR = 220       # largeur intérieure finie
SAC_HAUTEUR = 280       # hauteur intérieure finie (hors coulisse)
COULISSE_H = 30         # hauteur de la coulisse pour le cordon
OUVERTURE_COULISSE = 15 # fente pour passer le cordon

# === Couture ===
MARGE_COUTURE = 10      # marge de couture (mm)

# === Séparateur / poche intérieure ===
POCHE_LARGEUR = 220     # même largeur que le sac
POCHE_HAUTEUR = 100     # hauteur de la poche (pour les pions)
POCHE_RABAT = 20        # rabat du haut de la poche (ourlet)

# === Appliqué décoratif (feutrine, 4×4 cases) ===
APPLI_CASES = 4
APPLI_CASE_MM = 15      # 15mm par case
APPLI_TAILLE = APPLI_CASES * APPLI_CASE_MM  # 60mm

# === SVG ===
SVG_MARGIN = 15
COLOR_CUT = "#FF0000"
COLOR_MARK = "#0000FF"   # repères (gravure légère ou marquage)
COLOR_ENGRAVE = "#000000"
COLOR_FOLD = "#00AA00"   # lignes de pliage
STROKE_W = 0.3
DASH = "4,3"


def f(v):
    return f"{v:.1f}"


def corps_sac(x0, y0, label="Corps du sac"):
    """Patron d'un panneau du corps du sac (avec marge de couture)."""
    m = MARGE_COUTURE
    w = SAC_LARGEUR + 2 * m
    h = SAC_HAUTEUR + COULISSE_H + 2 * m
    elements = []

    # Contour de découpe
    elements.append(
        f'    <rect x="{f(x0)}" y="{f(y0)}" '
        f'width="{f(w)}" height="{f(h)}" '
        f'fill="none" stroke="{COLOR_CUT}" stroke-width="{STROKE_W}"/>')

    # Ligne de couture (intérieur)
    elements.append(
        f'    <rect x="{f(x0 + m)}" y="{f(y0 + m)}" '
        f'width="{f(w - 2*m)}" height="{f(h - 2*m)}" '
        f'fill="none" stroke="{COLOR_MARK}" stroke-width="0.2" '
        f'stroke-dasharray="{DASH}"/>')

    # Ligne de pliage coulisse
    y_coulisse = y0 + m + SAC_HAUTEUR
    elements.append(
        f'    <line x1="{f(x0 + m)}" y1="{f(y_coulisse)}" '
        f'x2="{f(x0 + w - m)}" y2="{f(y_coulisse)}" '
        f'stroke="{COLOR_FOLD}" stroke-width="0.2" '
        f'stroke-dasharray="{DASH}"/>')

    # Fentes pour le cordon (2 petites ouvertures)
    y_fente = y_coulisse + COULISSE_H / 2
    fx1 = x0 + m + SAC_LARGEUR * 0.3
    fx2 = x0 + m + SAC_LARGEUR * 0.7
    for fx in [fx1, fx2]:
        elements.append(
            f'    <line x1="{f(fx - OUVERTURE_COULISSE/2)}" y1="{f(y_fente)}" '
            f'x2="{f(fx + OUVERTURE_COULISSE/2)}" y2="{f(y_fente)}" '
            f'stroke="{COLOR_CUT}" stroke-width="{STROKE_W}"/>')

    # Label
    elements.append(
        f'    <text x="{f(x0 + w/2)}" y="{f(y0 - 3)}" '
        f'text-anchor="middle" font-size="4" fill="{COLOR_MARK}">'
        f'{label}</text>')

    return "\n".join(elements), w, h


def poche_interieure(x0, y0):
    """Patron du séparateur / poche intérieure."""
    m = MARGE_COUTURE
    w = POCHE_LARGEUR + 2 * m
    h = POCHE_HAUTEUR + POCHE_RABAT + m  # marge en bas, rabat en haut
    elements = []

    # Contour de découpe
    elements.append(
        f'    <rect x="{f(x0)}" y="{f(y0)}" '
        f'width="{f(w)}" height="{f(h)}" '
        f'fill="none" stroke="{COLOR_CUT}" stroke-width="{STROKE_W}"/>')

    # Ligne de pliage du rabat
    y_rabat = y0 + POCHE_RABAT
    elements.append(
        f'    <line x1="{f(x0)}" y1="{f(y_rabat)}" '
        f'x2="{f(x0 + w)}" y2="{f(y_rabat)}" '
        f'stroke="{COLOR_FOLD}" stroke-width="0.2" '
        f'stroke-dasharray="{DASH}"/>')

    # Label
    elements.append(
        f'    <text x="{f(x0 + w/2)}" y="{f(y0 - 3)}" '
        f'text-anchor="middle" font-size="4" fill="{COLOR_MARK}">'
        f'Poche intérieure (×1)</text>')

    return "\n".join(elements), w, h


def applique_damier(x0, y0):
    """Motif damier 4×4 en feutrine (découpe + gravure laser)."""
    n = APPLI_CASES
    sz = APPLI_CASE_MM
    total = APPLI_TAILLE
    elements = []

    # Contour de découpe (carré avec coins arrondis)
    r = 3  # rayon des coins
    elements.append(
        f'    <rect x="{f(x0)}" y="{f(y0)}" '
        f'width="{f(total)}" height="{f(total)}" rx="{r}" ry="{r}" '
        f'fill="none" stroke="{COLOR_CUT}" stroke-width="{STROKE_W}"/>')

    # Cases sombres (gravure)
    for row in range(n):
        for col in range(n):
            if (row + col) % 2 == 1:
                cx = x0 + col * sz
                cy = y0 + row * sz
                elements.append(
                    f'    <rect x="{f(cx)}" y="{f(cy)}" '
                    f'width="{f(sz)}" height="{f(sz)}" '
                    f'fill="{COLOR_ENGRAVE}" stroke="none"/>')

    # Label
    elements.append(
        f'    <text x="{f(x0 + total/2)}" y="{f(y0 - 3)}" '
        f'text-anchor="middle" font-size="4" fill="{COLOR_MARK}">'
        f'Appliqué feutrine (×1)</text>')

    return "\n".join(elements), total, total


def generate_svg():
    # Calculer les dimensions de chaque pièce
    m = MARGE_COUTURE
    corps_w = SAC_LARGEUR + 2 * m
    corps_h = SAC_HAUTEUR + COULISSE_H + 2 * m
    poche_w = POCHE_LARGEUR + 2 * m
    poche_h = POCHE_HAUTEUR + POCHE_RABAT + m
    appli_sz = APPLI_TAILLE

    # Disposition sur le SVG (2 corps côte à côte, poche et appliqué en dessous)
    gap = 20
    total_w = 2 * corps_w + gap + 2 * SVG_MARGIN
    total_h = (SVG_MARGIN + 10 + corps_h + gap + 10
               + max(poche_h, appli_sz) + SVG_MARGIN)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg"')
    parts.append(f'     width="{f(total_w)}mm" height="{f(total_h)}mm"')
    parts.append(f'     viewBox="0 0 {f(total_w)} {f(total_h)}">')
    parts.append('')

    # Corps du sac ×2
    y_top = SVG_MARGIN + 8
    c1, _, _ = corps_sac(SVG_MARGIN, y_top, "Corps du sac (×2 — pièce 1)")
    c2, _, _ = corps_sac(SVG_MARGIN + corps_w + gap, y_top,
                         "Corps du sac (×2 — pièce 2)")
    parts.append('  <g id="corps">')
    parts.append(c1)
    parts.append(c2)
    parts.append('  </g>')
    parts.append('')

    # Poche + Appliqué
    y_bottom = y_top + corps_h + gap + 8
    p, _, _ = poche_interieure(SVG_MARGIN, y_bottom)
    a, _, _ = applique_damier(SVG_MARGIN + poche_w + gap, y_bottom + 10)

    parts.append('  <g id="poche">')
    parts.append(p)
    parts.append('  </g>')
    parts.append('')
    parts.append('  <g id="applique">')
    parts.append(a)
    parts.append('  </g>')

    # Légende
    y_leg = total_h - SVG_MARGIN + 5
    parts.append('')
    parts.append('  <g id="legende" font-size="3.5">')
    parts.append(f'    <text x="{f(SVG_MARGIN)}" y="{f(y_leg)}" '
                 f'fill="{COLOR_CUT}">Rouge = découpe</text>')
    parts.append(f'    <text x="{f(SVG_MARGIN + 80)}" y="{f(y_leg)}" '
                 f'fill="{COLOR_MARK}">Bleu = repère couture</text>')
    parts.append(f'    <text x="{f(SVG_MARGIN + 170)}" y="{f(y_leg)}" '
                 f'fill="{COLOR_FOLD}">Vert = pliage</text>')
    parts.append(f'    <text x="{f(SVG_MARGIN + 240)}" y="{f(y_leg)}" '
                 f'fill="{COLOR_ENGRAVE}">Noir = gravure</text>')
    parts.append('  </g>')

    parts.append('')
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    svg = generate_svg()
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "pochette_patron.svg")
    with open(out_path, "w") as fh:
        fh.write(svg)

    m = MARGE_COUTURE
    print(f"SVG généré : {out_path}")
    print(f"\nPièces du patron :")
    print(f"  Corps du sac (×2) : {SAC_LARGEUR + 2*m} × "
          f"{SAC_HAUTEUR + COULISSE_H + 2*m} mm")
    print(f"    → fini : {SAC_LARGEUR} × {SAC_HAUTEUR} mm + "
          f"coulisse {COULISSE_H} mm")
    print(f"  Poche intérieure (×1) : {POCHE_LARGEUR + 2*m} × "
          f"{POCHE_HAUTEUR + POCHE_RABAT + m} mm")
    print(f"  Appliqué damier (×1) : {APPLI_TAILLE} × {APPLI_TAILLE} mm "
          f"(feutrine)")
    print(f"\nFournitures :")
    print(f"  Tissu coton/lin : ~50 × 70 cm")
    print(f"  Feutrine : chute de ~8 × 8 cm")
    print(f"  Cordon : ~60 cm (×2 si double cordon)")
    print(f"  Fil assorti")
    print(f"\nÉtapes de montage :")
    print(f"  1. Découper les pièces au laser (tissu + feutrine)")
    print(f"  2. Graver le damier sur l'appliqué feutrine")
    print(f"  3. Coudre l'appliqué sur la face avant du sac")
    print(f"  4. Coudre la poche intérieure sur la face arrière")
    print(f"  5. Assembler les 2 faces (endroit contre endroit)")
    print(f"  6. Retourner, plier la coulisse, coudre")
    print(f"  7. Passer le cordon, nouer")
