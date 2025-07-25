import math
import pandas as pd 

def resistance_flexion_compose(M, profile, fy, appuis, lo, section_trans, N, by, bz):
    section_class = None
    
    u_values = {1: 1, 2: 0.7, 3: 0.5, 4: 2}
    v_values = {1: 1, 2: 2, 3: 3}
    
    u = u_values.get(appuis, 1)
    v = v_values.get(section_trans, 1)
    
    listes = {
        "liste1": ["IPE 1", "IPN 1", "HE 1", "UPE 1", "UPN 1", "L1"],
        "liste2": ["IPE 2", "IPN 2", "HE 2", "UPE 2", "UPN 2", "L2"],
        "liste3": ["IPE", "IPEA", "HEA", "HEB", "HEM"]
    }
    
    for m in listes["liste3"]:
        df = pd.read_excel("Classe.xlsx", sheet_name=m)
        for i in range(len(df["Profile"])):
            if profile == df["Profile"].iloc[i]:
                section_class = df.iloc[i].get(f"My {fy}", None)
    
    for j in listes["liste1"]:
        df = pd.read_excel("BDDP.xlsx", sheet_name=j)
        for i in range(len(df["Profile"])):
            if profile == df["Profile"].iloc[i]:
                h, b, tf, tw = df.iloc[i][["h mm", "b mm", "Tf mm", "Tw mm"]]
                A = df.iloc[i]['Amm2x102'] * 100 
                break
    
    for k in listes["liste2"]:
        df = pd.read_excel("BDDP.xlsx", sheet_name=k)
        for i in range(len(df["Profile"])):
            if profile == df["Profile"].iloc[i]:
                Wel, Welz, Wply, Wplz = df.iloc[i][["Wely", "Welz", "Wply", "Wplz"]] * 1e3
                iz = df.iloc[i]["iz"] * 10
                beta_w = 1 if section_class in [1, 2] else Wel / Wply if section_class == 3 else Wel / Wply 
                break
    
    gamma_M0, gamma_M1 = 1, 1.1
    epsilon = math.sqrt(fy / 235)
    lambda1 = 93.6 * epsilon
    L = lo * u
    lambdalt = (L / iz) / (1 + (1 / 20) * ((L / iz) ** 2 / (h / tf) ** 2)) ** 0.25
    lambdalt_reduit = (lambdalt / lambda1) * math.sqrt(beta_w)
    
    mu_y = lambdalt_reduit * (2 * by - 4) + (Wply - Wel) / Wel
    mu_z = lambdalt_reduit * (2 * bz - 4) + (Wplz - Welz) / Welz
    
    qi = 1  # Initialisation 
    ky = 1 - (mu_y * N) / (qi * A * fy)
    kz = 1 - (mu_z * N) / (qi * A * fy)
    k_lt = 1  #  initialization
    
    N_pl = A * fy
    M_pl = Wply * fy
    M_el = Wel * fy
    M_z = Wplz * fy
    
    n = N / N_pl
    a = min(A / A, 0.5)
    
    if M <= M_pl * (1 - (N / N_pl) ** 2):
        if lambdalt_reduit >= 0.4:
            u_lt = 0.15 * lambdalt_reduit * beta_w - 0.15
            fi = 0.5 * (1 + v * (lambdalt_reduit - 0.2) + lambdalt_reduit ** 2)
            qi = 1 / (fi + math.sqrt(fi ** 2 + lambdalt_reduit ** 2))
            Aw = A - 2 * b * tf
            k_lt = 1 - (u_lt ** N / (qi * A * fy))
        
        My = M_pl * (1 - ((1 - n) / (1 - 0.5 * a)) ** 2)
        
        if v in [1, 2]:
            check = N / (qi * N_pl) + k_lt * My / (qi * M_pl) + kz * My / M_z
            if check <= gamma_M1:
                print("Profile verifie")
                return M_pl / gamma_M0, N_pl / gamma_M0
            else:
                print("Profile non verifie")
                return None
        elif v == 3:
            check = N / (qi * N_pl) + k_lt * My / (qi * M_el) + kz * My / M_z
            if check <= gamma_M1:
                print("Profile verifie a la flexion")
                return M_pl / gamma_M0, N_pl / gamma_M0
            else:
                print("Profile non verifie")
                return None
    else:
        if v in [1, 2]:
            check = N / (qi * N_pl) + ky * My / (qi * M_pl) + kz * My / M_z
            if check <= gamma_M1:
                print("Profile verifie")
                return M_pl / gamma_M0, N_pl / gamma_M0
            else:
                print("Profile non verifie")
                return None
        elif v == 3:
            check = N / (qi * N_pl) + ky * My / (qi * M_el) + kz * My / M_z
            if check <= gamma_M1:
                print("Profile verifie")
                return M_pl / gamma_M0, N_pl / gamma_M0
            else:
                print("Profile non verifie")
                return None

# Conversion des unités :
# M_pl est en N.mm, on divise par 10⁶ pour avoir des kN.m
# N_pl est en N, on divise par 10³ pour avoir des kN
resultat = resistance_flexion_compose(300,"IPE 200",200,1,2,1,100,1.3,1)
if resultat:
    M_pl_d, N_pl_d = resultat
    M_pl_d = M_pl_d / 1e6  # Conversion en kN.m
    N_pl_d = N_pl_d / 1e3  # Conversion en kN
    print(f"Moment resistant de calcul: {M_pl_d:.2f} kN.m")
    print(f"Effort normal resistant de calcul: {N_pl_d:.2f} kN")
