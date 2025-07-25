import flexion_pure_max
import pandas as pd
import os


def flexion_pure_dimensionnement(famille_profile, M_Ed, fy, appuis, lo, section_trans):
    A = "IPE 1"
    B = "IPN 1"
    C = "UPE 1"
    D = "HE 1"
    E = "L1"
    F = "UPN 1"
    G = "HL1"
    H = "HD1"
    I = "HP1"
    J = "U1"

    match famille_profile:
        case 1:
            famille = A
        case 2:
            famille = B
        case 3:
            famille = C
        case 4:
            famille = F
        case 5:
            famille = D
        case 6:
            famille = E
        case 7: 
            famille =  G
        case 8:
            famille = H
        case 9:
            famille = I
        case 10:
            famille = J
            
            


    df = pd.read_excel("Base_De_Données/BDDP.xlsx", sheet_name=famille)
    df = pd.DataFrame(df)

    result_message = ""
    for i in range(len(df["Profile"])):
        y = df["Profile"].iloc[i]
        result = flexion_pure_max.flexion_pure_max(y, fy, appuis, lo, section_trans)
        # result_message += f"Résistance pour {y}: {result} N.m\n"

        if result > M_Ed:
            profile_vérifié = df["Profile"].iloc[i]
            result_message += f"\nUtilisez le profilé {profile_vérifié} pour résister à la flexion pure\n"
            result_message += f"Moment résistant: {result:.2f} N.m ≥ {M_Ed:.2f} N.m"
            break
    
    return result_message  # Retourner le message complet



