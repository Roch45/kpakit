import math
import pandas as pd
import os
from utils import resource_path
from classe_profile import classe_profile

def flexion_pure_max(profile, fy, appuis, lo, section_trans):

    section_class = 1

    match appuis:
        case 1:
            u = 1
        case 2:
            u = 0.7
        case 3:
            u = 0.5
        case 4:
            u = 2

    liste2 = ["IPE 1", "IPN 1", "HE 1", "UPE 1", "UPN 1","HL1","HD1","HP1","U1","L1"]
    liste3 = ["IPE 2", "IPN 2", "HE 2", "UPE 2", "UPN 2","HL2","HD2","HP2","U2","L2"]
    

    section_class=classe_profile(profile,fy,"Flexion")
  

    for j in liste2:

        df = pd.read_excel(resource_path(os.path.join("Base_De_Données", "BDDP.xlsx")), sheet_name=j)
        df = pd.DataFrame(df)

        for i in range(len(df["Profile"])):
            if profile == df["Profile"].iloc[i]:
                try:
                    # Essayer d'abord avec "Tf mm"
                    [h, b, tf] = [df.iloc[i]["h mm"], df.iloc[i]["b mm"], df.iloc[i]["Tf mm"]]
                except KeyError:
                    try:
                        # Essayer avec "tf mm"
                        [h, b, tf] = [df.iloc[i]["h mm"], df.iloc[i]["b mm"], df.iloc[i]["tf mm"]]
                    except KeyError:
                        # Si toujours pas trouvé, afficher les colonnes disponibles
                        print("Colonnes disponibles:", df.columns.tolist())
                        raise ValueError(f"Impossible de trouver les colonnes nécessaires dans {j}")

    
    for k in liste3:

        df = pd.read_excel(resource_path(os.path.join("Base_De_Données", "BDDP.xlsx")), sheet_name=k)
        df = pd.DataFrame(df)

        for i in range(len(df["Profile"])):
            if profile == df["Profile"].iloc[i]:
                [Wel, Wpl] = [df.iloc[i]["Wely"]*1e3, df.iloc[i]["Wply"]*1e3]
                iz = df.iloc[i]["iz"]*10

    if section_class==1 or section_class==2:
        beta_w = 1
    elif section_class==3:
        beta_w = Wel/Wpl
    
    
    gamma_M0 = 1
    gamma_M1 = 1.1

    epsilon = math.sqrt(235/fy)

    lambda1 = 93.6 * epsilon 

    L = u*lo

    lambda_LT = (L / iz) / (1 + (1 / 20) * ((L / iz) ** 2 / (h / tf) ** 2)) ** 0.25

    # Calcul de lambda lt réduit
    lambda_LT_reduit = (lambda_LT/lambda1)*math.sqrt(beta_w)


    if lambda_LT_reduit < 0.4:
        if section_class==1 or section_class==2:
            M_Rd = (Wpl * fy) / gamma_M0
        elif section_class == 3:
            M_Rd = (Wel * fy) / gamma_M0

    else:
        alpha_lt = 0
        # Détermination de alpha_lt
        if section_trans == 1:
            if h/b <= 2: alpha_lt = 0.21
            else: alpha_lt = 0.34
        elif section_class == 2:
            if h/b <= 2: alpha_lt = 0.49
            else: alpha_lt = 0.76
        else: alpha_lt = 0.76
        

        # Calcul de fi
        fi_lt = 0.5 * (1 + alpha_lt * (lambda_LT_reduit-0.2) + lambda_LT_reduit**2)

        # Calcul de X_lt
        X_lt = 1 / (fi_lt + math.sqrt(fi_lt**2 - lambda_LT_reduit**2))

        # Calcul de M_Rd
        M_Rd = (X_lt * beta_w * Wpl * fy) / gamma_M1

    # Convert from N.mm to N.m
    return (M_Rd * 1e-3)


  


