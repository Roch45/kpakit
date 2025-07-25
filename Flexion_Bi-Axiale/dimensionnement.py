import pandas as pd
def verification(profilé,l,fy,My,Mz,N,section):
    import pandas as pd
    import math


    # veiller à ce que l'utilisateur entre une longeur de poutre correcte (pas de valeur négative ou de letrres)


    # Dataframes de la BDDP

    df=pd.read_excel("BDDP.xlsx",sheet_name=["IPE 1","IPE 2","HE 1","HE 2"],index_col="Profile") 

    # recherche des valeurs de iz, h et tf en fonction du profilé
    p = profilé.split() ; taille = len(p) ; iz = 0

    for feuille,dff in df.items():

        for idx in dff.index:

            if taille == 2 and (p[0] in idx and p[1] in idx)  and ("h mm" in dff.columns):
                h = dff.loc[idx,"h mm"]
                b = dff.loc[idx,"b mm"]
                tf = dff.loc[idx,"Tf mm "]
                A = dff.loc[idx,"Amm2x102"]*10**2
                tw = dff.loc[idx,"Tw mm"]
                d = dff.loc[idx,"d mm"]
            if taille == 2 and (p[0] in idx and p[1] in idx)  and ("iz" in dff.columns):
                iz = (dff.loc[idx,"iz"])/100    # x10/1000 pour l' obtenir en mètre(m). selon le tableau il doit etre multiplié 10 d'abord
                wply = dff.loc[idx,"Wply"]*10**3
                wplz = dff.loc[idx,"Wplz"]*10**3
                wely = dff.loc[idx,"Wely"]*10**3
                welz = dff.loc[idx,"Welz"]*10**3
                break
            if taille == 3 and (p[0] in idx and p[1] in idx and p[2] in idx)  and ("h mm" in dff.columns):
                h = dff.loc[idx,"h mm"]
                b = dff.loc[idx,"b mm"]
                tf = dff.loc[idx,"Tf mm "]
                A = dff.loc[idx,"Amm2x102"]*10**2
                tw = dff.loc[idx,"Tw mm"]
                d = dff.loc[idx,"d mm"]
            if taille == 3 and (p[0] in idx and p[1] in idx and p[2] in idx)  and ("iz" in dff.columns):
                iz = (dff.loc[idx,"iz"])/100    # x10/1000 pour l' obtenir en mètre(m). selon le tableau il doit etre multiplié 10 d'abord
                wply = dff.loc[idx,"Wply"]*10**3
                wplz = dff.loc[idx,"Wplz"]*10**3
                wely = dff.loc[idx,"Wely"]*10**3
                welz = dff.loc[idx,"Welz"]*10**3
                break
        if iz != 0:
            break
            
    
    # calcul de la valeur de lambda_lt

    lambda_lt = (l/iz)/(1+(1/20)*((l/iz)/(h/tf))**2)**0.25  
    
    # calcul de la valeur de epsilon selon la nuance d'acier biensur!!
    epsilon=math.sqrt(235/fy)

    # calcul de lambda_1
    lambda_1 = 93.6*epsilon


    # fontion déterminant les classes des profilés

    def classe(profilé,fy,N):
        df=pd.read_excel("classe_section_profilés.xlsx",sheet_name=None,index_col="Profile")
        if N == 0:
            x = 0                           
            for feuille,dff in df.items():     
                for idx in dff.index:
                    if profilé == idx:
                        dff_de_continuation = dff
                        idx_de_continuation = idx
                        x=1
                        break
                if x==1:
                    break
            colonne=[]
            for col in list(dff_de_continuation.columns):
                if str(fy) in col and not ("N" in col):
                    colonne += [col]
            liste_classe=[]
            for i in colonne:
                liste_classe += [dff_de_continuation.loc[idx_de_continuation,i]]
            
            classe_profilé =max (liste_classe)

            return classe_profilé
        elif N != 0:
            x = 0
            for feuille,dff in df.items():
                for idx in dff.index:
                    if profilé == idx:
                        dff_de_continuation = dff
                        idx_de_continuation = idx
                        x=1
                        break
                if x==1:
                    break
            colonne=[]
            for col in list(dff_de_continuation.columns):
                if str(fy) in col:
                    colonne += [col]
            liste_classe=[]
            for i in colonne:
                liste_classe += [dff_de_continuation.loc[idx_de_continuation,i]]
            
            classe_profilé = max(liste_classe)

            return classe_profilé
    
    # classe du profilé
    classe_profilé = classe(profilé,fy,N)

    # calcul du module efficace weff

    def weff_profilé(h,b,tw,tf,d,A,epsilon,axe):

        # semelle comprimée
        import math

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
        
        if axe == "y":
            return weff_y
        elif axe == "z":
            return weff_z
        elif axe == "A":
            return Aeff

    # calcul de beta_w en fonction de la classe du profilé
    
    if classe_profilé == 1 or classe_profilé == 2:

        beta_w=1
    elif classe_profilé == 3:

        beta_w = wely/wply
    elif classe_profilé == 4:
        # j'ai deja récupéré une fois h et tf 
        
        weff_y = weff_profilé(h,b,tw,tf,d,A,epsilon,"y")
        weff_z = weff_profilé(h,b,tw,tf,d,A,epsilon,"z") # je le récupère en meme temps car j'en aurai besoin un peu plus bas
        Meffy = weff_y*fy  # je le calcule car j'en aurai besoin si la classe est 4
        Meffz = weff_z*fy  # je le calcule car j'en aurai besoin si la classe est 4
        Aeff = weff_profilé(h,b,tw,tf,d,A,epsilon,"A")  # je le récupère en meme temps car j'en aurai besoin un peu plus bas
        beta_w = weff_y/(wply*10**3)
    
    # calcul de lambda_bar_lt
    lambda_bar_lt = (lambda_lt/lambda_1)*math.sqrt(beta_w)
    
    # alpha_lt
    if section == 1:
        if h/b <= 2:
            alpha_lt = 0.21
        elif h/b > 2:
            alpha_lt = 0.34
    elif section == 2:
        if h/b <= 2:
            alpha_lt = 0.49
        elif h/b > 2:
            alpha_lt = 0.76

    # phi_lt
    phi_lt = 0.5*(1 + alpha_lt*(lambda_bar_lt - 0.2) + lambda_bar_lt**2)

    # khi_lt
    khi_lt = 1/(phi_lt + math.sqrt(phi_lt**2 - lambda_bar_lt**2))
    gamma_m1 = 1.1

    # Mply
    Mply = wply*fy
    Mplz = wplz*fy
    

    # moments de résistance
    if lambda_bar_lt >= 0.4:

        MRy = khi_lt*beta_w*Mply/gamma_m1
        MRz = khi_lt*beta_w*Mplz/gamma_m1
    elif lambda_bar_lt < 0.4:

        MRy = Mply
        MRz = Mplz
    k = "non"
    # vérification en proprement dit 
    if N == 0 :
        alpha = 2
        beta = 1

        if classe_profilé == 1 or classe_profilé == 2:
            if (My/MRy)**alpha + (Mz/MRz)**beta <= 1:
                k = "oui"
                #print("Section vérifiée.La section pourra résister!")
            else:
                pass
                #print("La section ne pourra pas résister.")
        elif classe_profilé == 3:
            Mely = wely*fy
            Melz = welz*fy ; gamma_m0 = 1
            if (My/Mely) + (Mz/Melz) <= 1/gamma_m0 :
                k = "oui"
                #print("Section vérifiée.La section pourra résister!")
            else:
                pass
                #print("La section ne pourra pas résister.")
        elif classe_profilé == 4:
            if (My/Meffy) + (Mz/Meffz) <= 1/gamma_m1:
                k = "oui"
                #print("Section vérifiée.La section pourra résister!")
            else:
                pass
                #print("La section ne pourra pas résister.")
    elif N != 0:
        alpha =2 ; Npl = A*fy ;n = N/Npl ; 
        beta = 5*n
        if (classe_profilé == 1 or classe_profilé == 2) and n <= 1:
            Aw = A - 2*b*tf ; a = min([(Aw/A),0.5])
            MNy = Mply*(1 - ((1-n)/(1-0.5*a))**2)
            MNz = Mplz*(1 - ((n-a)/(1-a))**2)
            if (My/MNy)**alpha + (Mz/MNz)**beta <= 1 and beta >= 1:
                k = "oui"
                #print("Section vérifiée.La section pourra résister!")
            else:
                pass
                #print("La section ne pourra pas résister.")
        elif classe_profilé == 3:
            Mely = wely*fy
            Melz = welz*fy ; gamma_m0 = 1
            if (N/(A*fy)) + (My/Mely) + (Mz/Melz) <= 1/gamma_m0:
                k = "oui"
                #print("Section vérifiée.La section pourra résister!")
            else:
                pass
                #print("La section ne pourra pas résister.")
        elif classe_profilé == 4:
            
            if (N/Aeff*fy) + (My/Meffy) + (Mz/Meffz) <= 1/gamma_m1:
                k = "oui" 
                #print("Section vérifiée.La section pourra résister!")
            else:
                pass
                #print("La section ne pourra pas résister.")
    return k , A ,profilé
    


# veiller à ce que l'utilisateur entre une longueur de poutre correcte (pas de valeur négative ou de letrres)
while True:
        try:
            l=float(input("Quelle est la longueur en mètre(m) de la poutre?: "))
            if l <=0:
                raise ValueError("Erreur:Vous avez entré un nombre négatif ou 0! Veuillez entrer un nombre supérieur à 0.")
            break
        except ValueError as e:
            print("Erreur:vous n'avez pas entré un nombre correct!",":",e)

# veuiller à ce que l'utilsateur entre 235, 275 ou 355 selon la nuance d'acier (pas autre chose que ces trois valeurs)

while True:
    try:
        fy = int(input("Quelle est la nuance de l'acier? (S235, S275, S355)\n"
        "veuillez entrer juste 235, 275 ou 355 : "))

        if fy != 235 and fy != 275 and fy != 355 :
            raise ValueError("Vous devez entrer 235, 275 ou 355")
        break
    except ValueError as e:
        print("Vous devez entrer 235, 275 ou 355")

# les valeurs de My,Mz et N (eventuel) à envoyer à la fonction qui va déterminer la classe du profilé

# d'abord les valeurs de My et Mz et s'assurer que les valeurs entrées sont correctes
while True:

    try:
        My = float(input("Quelle est la valeur en N.m du moment My appliqué au tour de l'axe y?: "))
        Mz = float(input("Quelle est la valeur en N.m du moment Mz appliqué au tour de l'axe z?: "))
        if My <= 0 or Mz <= 0:
            raise ValueError('Vous ne devez pas entrer une valeur de moment inférieure ou égale à 0.')
        My = My*1000 # conversion en N.mm
        Mz = Mz*1000
        break
    except ValueError as e:
        print("Erreur: valeur incorrete.",e)

# ensuite demander à savoir s'il y a un éffort normal ou pas et s'assurer que les entrées sont correctes
    
while True:
    try:
        choix=int(input("Il y a-t-il un éffort normal?\n1-Oui\n2-Non\nEntrez 1 ou 2 selon votre choix: "))
        if choix != 1 and choix != 2:
            raise ValueError()
        break
    except ValueError:
        print("Erreur: vous devez entrer 1 ou 2")

# demander la valeur de N s'il y en a est s'assurer que l'entrée est correcte sinon N=0

if choix == 1:
    while True:
        try:
            N=float(input("Quelle est la valeur en newton(N) de l'éffort normal?: "))
            if N <= 0:
                raise ValueError("vous ne devez pas entrer une valeur d'éffort normal inférieur ou égale à zéro.")
            break
        except ValueError as e:
            print("Erreur: valeur incorrecte")
elif choix == 2:
    N = 0

# section laminée ou soudée
while True:
    try :
        section = int(input("Type de section\n1.Laminée\n2.Soudée\nEntrez 1 ou 2 selon votre choix: "))
        if section != 1 and section != 2:
            raise ValueError()
        break
    except ValueError :
        print("Erreur: vous n'avez pas entré 1 ou 2")


# dataframe de la base de donnée des classes
df2=pd.read_excel("classe_section_profilés.xlsx",sheet_name=None,index_col="Profile") 

s = 0

for feuille,dff in df2.items():

    for profilé in dff.index:
        k , A , profile = verification(profilé,l,fy,My,Mz,N,section)
        if k == "oui":
            s = 1
            break
    if s == 1:
        break

            
print(f"Le profilé {profile} suffira pour résister.")
