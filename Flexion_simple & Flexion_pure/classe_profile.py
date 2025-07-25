import math
import pandas as pd
import os
from utils import resource_path

def classe_profile(profile,fy,Effort):
    
    liste2 = ["IPE 1", "IPN 1", "HE 1", "UPE 1", "UPN 1","HL1","HD1","HP1","U1","L1"]

    for j in liste2:

        df = pd.read_excel("Base_De_Données/BDDP.xlsx", sheet_name=j)
        df = pd.DataFrame(df)

        if j=="L1":
            for i in range(len(df["Profile"])):
                if profile==df["Profile"].iloc[i]:
                    [c1, tf, tw, r] = [df.iloc[i]["b mm"], df.iloc[i]["Tf mm"], df.iloc[i]["Tw mm"],df.iloc[i]["r mm"]]
                    b  = c1 -r -tf
                    t1 = tf
                    t2 = tf
                    c2 = (b)
        else:
            for i in range(len(df["Profile"])):
                if profile == df["Profile"].iloc[i]:
                    [h, b, tf, tw, r,d] = [df.iloc[i]["h mm"], df.iloc[i]["b mm"], df.iloc[i]["Tf mm"], df.iloc[i]["Tw mm"], df.iloc[i]["r mm"],df.iloc[i]["d mm"]]
                    c1=d
                    t1=tw
                    t2=tf
                    c2=(b/2)-r


        
    epsilon=math.sqrt(235/fy)



    calcul_1=c1/t1

    #Flexion parois interne

    if calcul_1 <=72*epsilon:
        valeur_1=1
    elif 72*epsilon <= calcul_1 <= 83*epsilon:
        valeur_1=2
    elif 83*epsilon <= calcul_1 <= 124*epsilon:
        valeur_1=3
    else:
        valeur_1=4
    
    #Compression parois interne 

    if calcul_1 <=33*epsilon:
        valeur_3 = 1
    elif 33*epsilon <= calcul_1 <= 38*epsilon:
        valeur_3 = 2
    elif 38*epsilon <= calcul_1 <= 42*epsilon:
        valeur_3 = 3
    else:
        valeur_3 = 4

    calcul_2 = c2/t2

    #Flexion 

    if calcul_2 <=9*epsilon:
        valeur_2=1
    elif 9*epsilon <= calcul_2 <= 10*epsilon:
        valeur_2=2
    elif 10*epsilon <= calcul_2 <= 14*epsilon:
        valeur_2=3
    else:
        valeur_2=4

    #RETOUR DES VALEURS DES CLASSES

    if Effort=="Flexion":
        return(max(valeur_1,valeur_2))
    else:
        print("Briquette")
        return(max(valeur_3,valeur_2))
    
       