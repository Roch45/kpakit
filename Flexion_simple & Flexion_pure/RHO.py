import math
def calcul_rho_profil(type_profil, bf, tf, h, tw, fy, E=210000, debug=False):
    """
    Calcule les coefficients de réduction ρ_f et ρ_w (section efficace)
    pour un profilé en I, U ou H, selon EN 1993-1-1 Annexe B.

    Paramètres :
    - type_profil : 'I', 'U' ou 'H'
    - bf : largeur aile (mm)
    - tf : épaisseur aile (mm)
    - h  : hauteur totale (mm)
    - tw : épaisseur âme (mm)
    - fy : limite élastique (MPa)
    - E  : module de Young (par défaut 210000 MPa)
    - debug : affiche les calculs intermédiaires si True

    Retourne :
    - rho_f : coefficient de réduction aile comprimée
    - rho_w : coefficient de réduction âme comprimée
    """

    epsilon = math.sqrt(235 / fy)

    # Largeur comprimée de l’aile (demi-aile à cause de symétrie ou non)
    if type_profil.upper() == 'U':
        # profil U : une seule aile comprimée, bord libre
        b_f = bf  # toute l’aile est comprimée
    else:  # 'I' ou 'H'
        b_f = (bf - tw) / 2  # demi-aile

    # Hauteur comprimée de l’âme
    h_w = h - 2 * tf
    c_w = h_w / 2  # on suppose flexion autour axe fort
    

    # Élancement réduit pour l’aile
    lambda_p_f = (b_f / tf) / ((28.4 * epsilon) * math.sqrt(0.43))
    if lambda_p_f <= 0.673:
        rho_f = 1.0
    else:
        rho_f = (lambda_p_f - 0.055*(3 + lambda_p_f)) / (lambda_p_f**2)
        rho_f = max(0.0, min(rho_f, 1.0))

    # Élancement réduit pour l’âme
    lambda_p_w = (c_w / tw) / ((28.4 * epsilon) * math.sqrt(4.0))
    if lambda_p_w <= 0.673:
        rho_w = 1.0
    else:
        rho_w = (lambda_p_w - 0.055*(3 + lambda_p_w)) / (lambda_p_w**2)
        rho_w = max(0.0, min(rho_w, 1.0))

    if debug:
        print(f"[DEBUG] Profil {type_profil.upper()}")
        print(f"  b_f = {b_f:.2f} mm, λp_f = {lambda_p_f:.3f}, ρ_f = {rho_f:.3f}")
        print(f"  c_w = {c_w:.2f} mm, λp_w = {lambda_p_w:.3f}, ρ_w = {rho_w:.3f}")

    return rho_f, rho_w
