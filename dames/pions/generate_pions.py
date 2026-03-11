#!/usr/bin/env python3
"""
Générateur STL des pions pour jeu de dames de voyage.
Impression 3D sur Ultimaker 2+ Connect.

Génère :
  - pion.stl  : pion normal (cylindre plat avec chanfrein)
  - dame.stl  : dame/roi (plus haut, avec rainure distinctive)

Utilisation :
    python3 generate_pions.py
    → génère pion.stl et dame.stl dans le même répertoire
"""

import math
import os

# === Paramètres des pions ===
PION_DIAM = 15.0      # Diamètre du pion (mm)
PION_H = 5.0          # Hauteur du pion normal (mm)
DAME_H = 8.0          # Hauteur de la dame (mm)
CHANFREIN = 0.8       # Chanfrein sur le dessus (mm)
RAINURE_PROF = 1.0    # Profondeur de la rainure (dame)
RAINURE_LARG = 1.5    # Largeur de la rainure (dame)
RAINURE_POS = 3.0     # Position depuis le haut (dame)
N_SEG = 48            # Segments du cercle


def cylinder_stl(name, diameter, height, chanfrein=0.0,
                 rainure=None, n_seg=N_SEG):
    """Génère un cylindre en STL ASCII avec chanfrein optionnel et rainure.

    rainure: dict(pos, largeur, profondeur) ou None
      pos = distance depuis le sommet
      Le profil du cylindre devient :
        base → sous_rainure → fond_rainure → haut_rainure → chanfrein → sommet
    """
    r = diameter / 2.0
    facets = []

    # Profil en coupe (liste de (rayon, hauteur) du bas vers le haut)
    profile = [(r, 0.0)]  # base

    if rainure:
        rp = rainure["pos"]
        rl = rainure["largeur"]
        rd = rainure["profondeur"]
        # Sous la rainure
        profile.append((r, height - rp - rl))
        # Fond de rainure
        profile.append((r - rd, height - rp - rl))
        profile.append((r - rd, height - rp))
        # Au-dessus de la rainure
        profile.append((r, height - rp))

    if chanfrein > 0:
        profile.append((r, height - chanfrein))
        profile.append((r - chanfrein, height))
    else:
        profile.append((r, height))

    # Générer les angles
    angles = [2 * math.pi * i / n_seg for i in range(n_seg)]

    def pt(radius, h, a):
        return (radius * math.cos(a), radius * math.sin(a), h)

    def facet(p1, p2, p3):
        # Calcul de la normale
        u = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
        v = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
        n = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        ln = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
        if ln > 0:
            n = (n[0]/ln, n[1]/ln, n[2]/ln)
        return (n, p1, p2, p3)

    # Face inférieure (z=0)
    center_bot = (0, 0, 0)
    for i in range(n_seg):
        a1 = angles[i]
        a2 = angles[(i + 1) % n_seg]
        p1 = pt(r, 0, a2)  # ordre inverse pour normale vers le bas
        p2 = pt(r, 0, a1)
        facets.append(facet(center_bot, p1, p2))

    # Faces latérales (entre chaque niveau du profil)
    for lvl in range(len(profile) - 1):
        r1, h1 = profile[lvl]
        r2, h2 = profile[lvl + 1]
        for i in range(n_seg):
            a1 = angles[i]
            a2 = angles[(i + 1) % n_seg]
            bl = pt(r1, h1, a1)
            br = pt(r1, h1, a2)
            tl = pt(r2, h2, a1)
            tr = pt(r2, h2, a2)
            facets.append(facet(bl, br, tr))
            facets.append(facet(bl, tr, tl))

    # Face supérieure
    top_r, top_h = profile[-1]
    center_top = (0, 0, top_h)
    for i in range(n_seg):
        a1 = angles[i]
        a2 = angles[(i + 1) % n_seg]
        p1 = pt(top_r, top_h, a1)
        p2 = pt(top_r, top_h, a2)
        facets.append(facet(center_top, p1, p2))

    # Écriture STL ASCII
    lines = [f"solid {name}"]
    for n, p1, p2, p3 in facets:
        lines.append(f"  facet normal {n[0]:.6f} {n[1]:.6f} {n[2]:.6f}")
        lines.append("    outer loop")
        lines.append(f"      vertex {p1[0]:.6f} {p1[1]:.6f} {p1[2]:.6f}")
        lines.append(f"      vertex {p2[0]:.6f} {p2[1]:.6f} {p2[2]:.6f}")
        lines.append(f"      vertex {p3[0]:.6f} {p3[1]:.6f} {p3[2]:.6f}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {name}")
    return "\n".join(lines)


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # Pion normal
    stl = cylinder_stl("pion", PION_DIAM, PION_H, chanfrein=CHANFREIN)
    path = os.path.join(out_dir, "pion.stl")
    with open(path, "w") as fh:
        fh.write(stl)
    print(f"Généré : {path}")
    print(f"  Pion : diam {PION_DIAM}mm, hauteur {PION_H}mm, "
          f"chanfrein {CHANFREIN}mm")

    # Dame
    stl = cylinder_stl("dame", PION_DIAM, DAME_H, chanfrein=CHANFREIN,
                        rainure={"pos": RAINURE_POS,
                                 "largeur": RAINURE_LARG,
                                 "profondeur": RAINURE_PROF})
    path = os.path.join(out_dir, "dame.stl")
    with open(path, "w") as fh:
        fh.write(stl)
    print(f"Généré : {path}")
    print(f"  Dame : diam {PION_DIAM}mm, hauteur {DAME_H}mm, "
          f"rainure à {RAINURE_POS}mm du sommet")

    print(f"\nPour un jeu complet : 12 pions + 12 pions (2 couleurs)")
    print(f"Prévoir quelques dames de réserve par couleur")
    print(f"Imprimer en 2 couleurs de PLA sur les 2 Ultimaker")
