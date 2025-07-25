import flexion_pure_max
import flexion_pure_vérification
import flexion_pure_dimensionnement
import flexion_simple_max
import flexion_simple_vérification
import flexion_simple_dimensionnement   

Go = int(input("Votre opération (Choississez entre 1, 2, 3, 4, 5 ou 6):\n 1: Flexion pure vérification\n 2: Flexion pure Moment résistant max \n 3: Flexion pure dimensionnement\n 4: Flexion simple vérification\n 5: Flexion simple (Effort et moment max)\n 6: Flexion simple dimensionnement\nVotre choix : "))

if Go in [1, 2, 4, 5]:
    profile = input('votre profilé : ')

fy = int(input('La nuance de l\'acier (235, ou 275 ou 355): S ? '))
appuis = int(input("Les types d'appuis, Choisir (1, 2, 3 ou 4)\n1: Articulé-Articulé \n2: Encastré-Artuculé \n3: Encastré-Encastré \n4: Encastré-Libre \nVotre choix : "))
lo = float(input("Longueur de la poutre : "))

if Go in [1, 2, 3]:
    section_trans = int(input("Le type de section transversale, Choisir (1, 2 ou 3) \n1: Section en I laminées \n2: Section en I soudées \n3: Autres section \nVotre choix : "))

match Go:
    case 1:
        M_Ed = float(input("Le moment fléchissant M_Ed généré : "))
        flexion_pure_vérification.flexion_pure_vérification(M_Ed, profile, fy, appuis, lo, section_trans)
    case 2:
        M_Rd = flexion_pure_max.flexion_pure_max(profile, fy, appuis, lo, section_trans)
        print("La résistance maximale est : ", M_Rd, "N.m pour le profilé choisi")
    case 3:
        M_Ed = float(input("Le moment fléchissant M_Ed généré : "))
        famille_profile = int(input('choisir parmir les profilés disponible\n1: IPE\n2 :IPN\n3 :UPE\n4 :UPN\n5 :HE\n6 L\n7 :HP\n8 :HD\n9 HL\n10 U\nVotre choix:\t : '))
        flexion_pure_dimensionnement.flexion_pure_dimensionnement(famille_profile, M_Ed, fy ,appuis ,lo ,section_trans)  
    case 4:
        M_Ed = float(input("Le moment fléchissant M_Ed généré : "))
        Ved=int(input("Valeur de l'effort tranchant généré V_Ed par les forces: "))
        section_trans2 = int(input("Le type de section transversale, Choisir (1, 2 ou 3) \n1: Section en I et H \n2: Profil en U laminés  \n3: Pour les cornière \nVotre choix : "))
        section_trans = int(input("Le type de section transversale, Choisir (1, 2 ou 3) \n1: Section en I laminées \n2: Section en I soudées \n3: Autres section \nVotre choix : "))
        flexion_simple_vérification.flexion_simple_vérification(M_Ed, Ved, profile, fy, appuis, lo, section_trans, section_trans2)
    case 5:
        section_trans2 = int(input("Le type de section transversale, Choisir (1, 2 ou 3) \n1: Section en I et H \n2: Profil en U laminés  \n3: Pour les cornière \nVotre choix : "))
        section_trans = int(input("Le type de section transversale, Choisir (1, 2 ou 3) \n1: Section en I laminées \n2: Section en I soudées \n3: Autres section \nVotre choix : "))
        [M_Rd, Vpl_Rd] = flexion_simple_max.flexion_simple_max(profile, fy, appuis, lo, section_trans, section_trans2)
        print("La résistance maximale est : ", M_Rd, "N.m pour le profilé choisi")
        print("L'effort tranchant maximale est : ", Vpl_Rd, "N pour le profilé choisi")
    case 6:
        M_Ed = float(input("Le moment fléchissant M_Ed généré : "))
        Ved=int(input("Valeur de l'effort tranchant généré V_Ed par les forces: "))
        section_trans2 = int(input("Le type de section transversale, Choisir (1, 2 ou 3) \n1: Section en I et H \n2: Profil en U laminés  \n3: Pour les cornière \nVotre choix : "))
        section_trans = int(input("Le type de section transversale, Choisir (1, 2 ou 3) \n1: Section en I laminées \n2: Section en I soudées \n3: Autres section \nVotre choix : "))
        famille_profile = int(input('choisir parmir les profilés disponible\n1: IPE\n2 :IPN\n3 :UPE\n4 :UPN\n5 :HE\n6 L\n7 :HP\n8 :HD\n9 HL\n10 U\nVotre choix:\t : '))
        flexion_simple_dimensionnement.flexion_simple_dimensionnement(famille_profile, M_Ed, Ved, fy, appuis, lo, section_trans, section_trans2)
    case _:
        print("Choix invalide")

