import flexion_simple_max
import pandas as pd
import os


def flexion_simple_dimensionnement(famille_profile, M_Ed, Ved, fy, appuis, lo, section_trans, section_trans2):

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
    profile_trouve = False
    
    for i in range(len(df["Profile"])):
        y = df["Profile"].iloc[i]
        [M_Rd, Vpl_Rd] = flexion_simple_max.flexion_simple_max(y, fy, appuis, lo, section_trans, section_trans2)
        # result_message += f"Test du profilé {y}:\n"
        # result_message += f"M_Rd = {M_Rd:.2f} N.m, Vpl_Rd = {Vpl_Rd:.2f} N\n"
        
        if M_Rd >= M_Ed and Vpl_Rd >= Ved:
            profile_verifie = df["Profile"].iloc[i]
            result_message += f"\n✅ Profilé optimal trouvé: {profile_verifie}\n"
            result_message += f"Moment résistant: {M_Rd:.2f} N.m ≥ {M_Ed:.2f} N.m\n"
            result_message += f"Effort tranchant résistant: {Vpl_Rd:.2f} N ≥ {Ved:.2f} N"
            profile_trouve = True
            break
    
    if not profile_trouve:
        result_message += "\n❌ Aucun profilé de cette famille ne peut résister aux efforts donnés"
    
    return result_message



