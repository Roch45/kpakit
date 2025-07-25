import math
import pandas as pd
import os
from utils import resource_path




def Efficace(profile,axe,fy,classe):
        
    liste2 = ["IPE 1", "IPN 1", "HE 1", "UPE 1", "UPN 1","HL1","HD1","HP1","U1","L1"]

    for j in liste2:

        df = pd.read_excel("Base_De_Données/BDDP.xlsx", sheet_name=j)
        df = pd.DataFrame(df)

        if j=="L1":
            for i in range(len(df["Profile"])):
                if profile==df["Profile"].iloc[i]:
                    [b, tf, tw, r, A, r2] = [df.iloc[i]["b mm"], df.iloc[i]["Tf mm"], df.iloc[i]["Tw mm"],df.iloc[i]["r mm"],df.iloc[i]["Amm2x102"],df.iloc[i]["r2 mm "]]
                    d=b-r-tf
                    h=b

        
        else:
            for i in range(len(df["Profile"])):
                if profile == df["Profile"].iloc[i]:
                    [h, b, tf, tw, r, d, A] = [df.iloc[i]["h mm"], df.iloc[i]["b mm"], df.iloc[i]["Tf mm"], df.iloc[i]["Tw mm"], df.iloc[i]["r mm"],df.iloc[i]["d mm"],df.iloc[i]["Amm2x102"]*1e2]
                   


    epsilon=math.sqrt(fy/235)

    # semelle comprimée
        

    spi = 1 ; k_sigma = 0.43; c = b/2 - tf/2 ; t = tf
    lambda_p = (c/t)/(28.4*epsilon*math.sqrt(k_sigma))
    rho = (lambda_p - 0.22)/lambda_p**2
    beff = rho*c
    beff_prime = rho*c

    # calcul de x 
    G = h/2
    G_1 = (tf*b*(tf/2) + (h-2*tf)*tw*(h/2) + (beff*2+tw)*tf*(h-tf/2))/(tf*b + (h-2*tf)*tw + (beff*2+tw)*tf)
    x = abs(G - G_1)
    v_s = h/2 + x
    v_i = h/2 - x
    spi = -(v_i/v_s)

    # ame fléchie
    k_sigma = 7.81 - 6.29*spi + 9.78*spi**2 ; t = tw
    lambda_p = (d/t)/(28.4*epsilon*math.sqrt(k_sigma))
    rho = (lambda_p - 0.22)/lambda_p**2
    beff = rho*(d/t)/2
    be1 = 0.4*beff
    be2 = 0.6*beff

    # centre de gravité G_2 et e
    numérateur = (b*tf*tf/2 + (be2+(h-2*tf)/2)*tw*(be2+(h-2*tf)/2+tf) + be1*tw*(h-be1/2-tf) +(beff_prime*2+tw)*tf*(h-tf/2) )
    déno = (b*tf + (be2+(h-2*tf)/2)*tw + be1*tw + (beff_prime*2+tw)*tf)
    G_2 = numérateur/déno
    x_1 = abs(G_2 - G)
    
    # module de résistance efficace y
    i1 = (b*tf**3)/12 + b*tf*(h/2-x_1-tf/2)**2
    i2 = (tw*((h-2*tf)/2 + be2)**3)/12 + tw*((h-2*tf)/2 + be2)*(h/2-x_1-((h-2*tf)/2 + be2)/2-tf)**2
    i3 = (tw*be1**3)/12 + tw*be1*(h/2-tf-be1/2 + x_1)**2
    i4 = (beff_prime*tf**3)/12 + beff_prime*tf*(h/2 - tf/2 + x_1)
    ieff_y = i1 + i2 + i3 + i4
    vs = h/2 + x_1
    v_i = h/2 - x_1
    weff_y = ieff_y/vs

    # module de résistance efficace z
    i1 = (tf*b**3)/12
    i2 = (((h-2*tf)/2 + be2)*tw**3)/12
    i3 = (be1*tw**3)/12
    i4 = (tf*beff_prime**3)/12
    ieff_z = i1 + i2 + i3 + i4
    weff_z = ieff_z/(b/2)

    # Aeff
    Aeff = A - (b-beff_prime)*tf -((A-2*b*tf)/2 - beff*tw)

    #Retour des résultat

    if classe ==4:

        if axe == "y":
            return [weff_y,Aeff]
        elif axe == "z":
            return [weff_z,Aeff] 
        
    else:
        return [0,0]