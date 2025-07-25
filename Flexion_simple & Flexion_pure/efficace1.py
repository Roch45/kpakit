from RHO import calcul_rho_profil


def section_efficace_profil(type_profil, bf, tf, h, tw, fy):
    """
    Calcule A_eff et W_eff pour profilés en I, H ou U en flexion autour de l'axe fort.
    
    Paramètres:
    - type_profil : 'I', 'H' ou 'U'
    - bf : largeur aile (mm)
    - tf : épaisseur aile (mm)
    - h : hauteur totale (mm)
    - tw : épaisseur âme (mm)
    - rho_f : coefficient de réduction aile comprimée (0 < rho_f <= 1)
    - rho_w : coefficient de réduction âme comprimée (0 < rho_w <= 1)
    
    Retourne:
    - A_eff : aire efficace totale (mm²)
    - W_eff : module de résistance efficace (mm³)
    """
    [rho_f, rho_w]=calcul_rho_profil(type_profil, bf, tf, h, tw, fy, E=210000, debug=False)
    # Dimensions efficaces des parties comprimées
    bf_eff = rho_f * bf
    # Pour âme, on considère la moitié supérieure comprimée (flexion autour axe fort)
    hw = h - 2 * tf
    hw_eff = rho_w * (hw / 2)

    # Aires efficaces des éléments
    # Aile sup (compressée)
    A_fs = bf_eff * tf
    # Ame sup (compressée)
    A_ws = hw_eff * tw
    # Ame inf (tendue)
    A_wi = (hw / 2) * tw
    # Aile inf (tendue)
    A_fi = bf * tf

    # Calcul de l'aire totale efficace
    A_eff = A_fs + A_ws + A_wi + A_fi

    # Calcul de la position de la fibre neutre efficace (prise depuis la base)
    # Positions moyennes des éléments (distance depuis la base)
    y_fi = tf / 2  # milieu aile inf
    y_wi = hw / 4 + tf  # milieu ame inf
    y_ws = h - (hw_eff / 2) - tf  # milieu ame sup (avec largeur efficace)
    y_fs = h - (tf / 2)  # milieu aile sup

    y_eff = (A_fi * y_fi + A_wi * y_wi + A_ws * y_ws + A_fs * y_fs) / A_eff

    # Calcul moment d'inertie efficace autour de la fibre neutre
    def I_plaque(b, e, y_c, y_n):
        # Inertie plaque autour de son centre + théorème des axes parallèles
        I_cent = (b * e**3) / 12
        A = b * e
        d = abs(y_c - y_n)
        return I_cent + A * d**2

    I_fs = I_plaque(bf_eff, tf, y_fs, y_eff)
    I_ws = I_plaque(tw, hw_eff, y_ws, y_eff)
    I_wi = I_plaque(tw, hw/2, y_wi, y_eff)
    I_fi = I_plaque(bf, tf, y_fi, y_eff)

    I_eff = I_fs + I_ws + I_wi + I_fi

    # Distance max entre la fibre neutre et la fibre la plus sollicitée
    # On prend la plus grande distance entre y_eff et base ou sommet
    y_top = h - y_eff
    y_bot = y_eff

    y_max = max(y_top, y_bot)

    # Module de résistance efficace
    W_eff = I_eff / y_max

    return A_eff, W_eff