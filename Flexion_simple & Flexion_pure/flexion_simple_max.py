import flexion_pure_max
import pandas as pd
import os
from utils import resource_path


def Tranchant_verification(profile, fy, section_trans2, nature=1, effort_direction=1):

    liste2 = ["IPE 1", "IPN 1", "HE 1", "UPE 1", "UPN 1","HL1","HD1","HP1","U1"]
    
    



    for j in liste2:

        df = pd.read_excel(resource_path(os.path.join("Base_De_Données", "BDDP.xlsx")), sheet_name=j)
        df = pd.DataFrame(df)

        for i in range(len(df["Profile"])):
            if profile == df["Profile"].iloc[i]:
                [h, b, tf, tw, aire] = [df.iloc[i]["h mm"], df.iloc[i]["b mm"], df.iloc[i]["Tf mm"], df.iloc[i]["Tw mm"], df.iloc[i]["Amm2x102"]*1e2]

    if section_trans2 == 1:
        if nature == 1:  # Laminé
            Av = 1.04*h*tw
        else:  # Reconstitué
            if effort_direction == 1:  # Parallèle à l'âme
                Av = (h-2*tf)*tw
            else:  # Parallèle aux semelles
                Av = aire-(h-2*tf)*tw
    elif section_trans2 == 2:
        Av = 1.04*h*tf
    elif section_trans2 == 3:
        Av = aire*h/(b+h)

    gamma_mo = 1
    
    #Calcul de Vpl_Rd
    Vpl_Rd = 0.58*(fy*Av)/gamma_mo

    return (Vpl_Rd)




def flexion_simple_max(profile, fy, appuis, lo, section_trans, section_trans2, nature=1, effort_direction=1):
    M_Rd = flexion_pure_max.flexion_pure_max(profile, fy, appuis, lo, section_trans)
    Vpl_Rd = Tranchant_verification(profile, fy, section_trans2, nature, effort_direction)

    return ([M_Rd, Vpl_Rd])
    