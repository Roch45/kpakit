from classe_profile import classe_profile
from efficace1 import section_efficace_profil
from RHO import calcul_rho_profil
from valeur_efficace import Efficace
import pandas as pd
import os
from utils import resource_path

liste2 = ["IPE 1", "IPN 1", "HE 1", "UPE 1", "UPN 1","HL1","HD1","HP1","U1"]
liste_I = ["IPE 1", "IPN 1"]
liste_U = ["UPE 1", "UPN 1","U1"]
liste_H = ["HL1","HD1","HP1", "HE 1"]
    

for j in liste2:

        df = pd.read_excel(os.path.join("Base_De_Données", "BDDP.xlsx"), sheet_name=j)

        df = pd.DataFrame(df)

        for i in range(len(df["Profile"])):
            
                [h, b, tf, tw, aire] = [df.iloc[i]["h mm"], df.iloc[i]["b mm"], df.iloc[i]["Tf mm"], df.iloc[i]["Tw mm"], df.iloc[i]["Amm2x102"]*1e2]

                if j == "IPE 1" or j== "IPN 1":
                     type_profil ="I"
                elif j== "UPE 1"or j == "UPN 1" or j == "U1":
                     type_profil ="U"
                elif j== "HL1"or j == "HD1"or j== "HP1" or j== "HE 1":
                     type_profil = "H" 

                [rho_f, rho_w]=calcul_rho_profil(type_profil, b, tf, h, tw, 235, E=210000, debug=False)

                A_eff, W_eff = section_efficace_profil(type_profil, b, tf, h, tw, 235)

                print(df.iloc[i]["Profile"],"\t","A_eff = ",A_eff," ","W_eff = ",W_eff)