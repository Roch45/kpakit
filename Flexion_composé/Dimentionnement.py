import math
import pandas as pd
import os

def dimensionnement(profilé, l, fy, My, Mz, N, section):
    # Vérification de l'existence du fichier Excel
    if not os.path.exists("BDDP.xlsx"):
        raise FileNotFoundError("Le fichier 'BDDP.xlsx' est introuvable.")

    # Lecture des données
    df = pd.read_excel("BDDP.xlsx", sheet_name=["IPE 1", "IPE 2", "HE 1", "HE 2"], index_col="Profile")

    # Recherche des caractéristiques du profilé
    p = profilé.split()
    taille = len(p)
    iz = 0

    for feuille, dff in df.items():
        for idx in dff.index:
            if all(part in idx for part in p):
                if "h mm" in dff.columns:
                    h = dff.loc[idx, "h mm"]
                    b = dff.loc[idx, "b mm"]
                    tf = dff.loc[idx, "Tf mm"]  # Suppression des espaces
                    A = dff.loc[idx, "Amm2x102"] * 10**2
                    tw = dff.loc[idx, "Tw mm"]
                    d = dff.loc[idx, "d mm"]
                
                if "iz" in dff.columns:
                    iz = dff.loc[idx, "iz"] / 100  # Conversion en mètres
                    wply = dff.loc[idx, "Wply"] * 10**3
                    wplz = dff.loc[idx, "Wplz"] * 10**3
                    wely = dff.loc[idx, "Wely"] * 10**3
                    welz = dff.loc[idx, "Welz"] * 10**3
                    break

        if iz != 0:
            break
    
    if iz == 0:
        raise ValueError(f"Profilé {profilé} introuvable dans les données.")

    # Calculs liés au flambement latéral
    lambda_lt = (l / iz) / (1 + (1 / 20) * ((l / iz) / (h / tf)) ** 2) ** 0.25
    epsilon = math.sqrt(235 / fy)
    lambda_1 = 93.6 * epsilon

    # Détermination de la classe du profilé
    def classe(profilé, fy, N):
        df_classe = pd.read_excel("Classe.xlsx", sheet_name=None, index_col="Profile")
        for feuille, dff in df_classe.items():
            if profilé in dff.index:
                colonnes_fy = [col for col in dff.columns if str(fy) in col and ("N" not in col or N != 0)]
                if colonnes_fy:
                    return max(dff.loc[profilé, colonnes_fy])
        return None

    classe_profilé = classe(profilé, fy, N)
    if classe_profilé is None:
        raise ValueError(f"Impossible de déterminer la classe du profilé {profilé}.")

    # Calcul de beta_w
    beta_w = 1 if classe_profilé in [1, 2] else wely / wply

    # Calcul de lambda_bar_lt
    lambda_bar_lt = (lambda_lt / lambda_1) * math.sqrt(beta_w)

    # Détermination de alpha_lt en fonction de la section
    alpha_lt = 0.21 if (section == 1 and h / b <= 2) else (0.34 if section == 1 else (0.49 if h / b <= 2 else 0.76))

    # Calcul des facteurs de réduction
    phi_lt = 0.5 * (1 + alpha_lt * (lambda_bar_lt - 0.2) + lambda_bar_lt**2)
    khi_lt = 1 / (phi_lt + math.sqrt(phi_lt**2 - lambda_bar_lt**2))
    gamma_m1 = 1.1

    # Calcul des moments plastiques
    Mply = wply * fy
    Mplz = wplz * fy

    # Détermination des moments de résistance
    if lambda_bar_lt >= 0.4:
        MRy = khi_lt * beta_w * Mply / gamma_m1
        MRz = khi_lt * beta_w * Mplz / gamma_m1
    else:
        MRy, MRz = Mply, Mplz

    # Vérification de la résistance
    k = "non"
    if N == 0:
        alpha, beta = 2, 1
        if classe_profilé in [1, 2] and (My / MRy) ** alpha + (Mz / MRz) ** beta <= 1:
            k = "oui"
        elif classe_profilé == 3:
            Mely, Melz, gamma_m0 = wely * fy, welz * fy, 1
            if (My / Mely) + (Mz / Melz) <= 1 / gamma_m0:
                k = "oui"
    else:
        alpha, beta = 2, 5 * (N / (A * fy))
        if classe_profilé in [1, 2] and (N / (A * fy)) <= 1:
            Aw = A - 2 * b * tf
            a = min([Aw / A, 0.5])
            MNy = Mply * (1 - ((1 - (N / (A * fy))) / (1 - 0.5 * a)) ** 2)
            MNz = Mplz * (1 - ((N / (A * fy) - a) / (1 - a)) ** 2)
            if (My / MNy) ** alpha + (Mz / MNz) ** beta <= 1 and beta >= 1:
                k = "oui"
        elif classe_profilé == 3:
            Mely, Melz, gamma_m0 = wely * fy, welz * fy, 1
            if (N / (A * fy)) + (My / Mely) + (Mz / Melz) <= 1 / gamma_m0:
                k = "oui"

    return k, round(float(A), 2), profilé



resultat = dimensionnement("IPE 160",2,235,200,40,200,2)
print(f"Résistance : {resultat[0]}")
print(f"Aire : {resultat[1]} mm²")
print(f"Profilé : {resultat[2]}")