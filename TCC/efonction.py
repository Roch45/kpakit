
from re import T
import pandas as ezdp
gamaMo=1
gamaM1=1.1
gamaM2=1.25
gamaMbc=1.25
gamaMbt=1.5

def menu():
    print("Bienvenue sur notre programme de dimenssionnement et vérification d'ossature en construction métallique. \nQuel silictiation vous interrese?")
    print("    1.Traction\n    2.Compression\n    3.Cissallement\n")
    ch=int(input("Que choississez vous?:  "))
    if(ch==1 or ch==2):
        tch=input("Que voulez vous faire? \nA. Dimenssionnement\nB. Verification\nVeuillez faire votre choix:").upper()
    return ch,tch
def recupMenu(c):
    if(c==1):
        
        ret=list()
        ret1=list()
        ret2=list()
        e1=int(input("D'accord c'est la traction entre ?\n1. Plat-Plal\n2. Deux plats - Un plal\n3. Plat-Corniere\n Choisissez:"))
        match e1:
            case 1:
                L1=int(input("Plat-Plat okay! Bon on va prendre les dimensions du premier plat. \nLongueur:"))
                l1=int(input("Largueur:"))
                t1=int(input("Epaisseur:"))
                s1=int(input("n'oublions pas un detail impotrant: la nuance. veuillez choisir: \n1. S235\n2. S275\n3. S355"))

                L2=int(input("On passe au second. Longueur:"))
                l2=int(input("Largeur:"))
                t2=int(input("Epaisseur:"))
                s2=int(input("n'oublions pas un detail impotrant: la nuance. veuillez choisir: \n1. S235\n2. S275\n3. S355"))
            case 2:
                L1=int(input("deux Plats- Un Plat okay! Bon on va prendre les dimensions du premier plat situé seul. \nLongueur:"))
                l1=int(input("Largueur:"))
                t1=int(input("Epaisseur:"))
                s1=int(input("n'oublions pas un detail impotrant: la nuance. veuillez choisir: \n1. S225\n2. S275\n3. S355"))

                L2=int(input("On passe au deux seconds qui sont identiques. Longueur:"))
                l2=int(input("Largeur:"))
                t2=int(input("Epaisseur:"))
                s2=int(input("n'oublions pas un detail impotrant: la nuance. veuillez choisir: \n1. S225\n2. S275\n3. S355 \n Choisissez:"))
        print("Ces élément sont associcé par des boulons ordinaires.")
        n=int(input("Nombre de boulons:"))
        phi=int(input("Diamétre des boulons: "))
        nc=int(input("Il sont rangé en :\n1. Rangé\n2 Quinconce\n Choisissez:"))
        ncn=0
        match nc:
            case 1:
                ncn=int(input("Rangé de combien de boulon?  "))
            case 2:
                print("Quinconce, voila qui complique les chose")
        ret.append([L1,l1,t1,s1])
        ret.append([L2,l2,t2,s2])
        return [[L1,l1,t1,s1],[L2,l2,t2,s2],[n,phi,nc,ncn,e1]]    
    elif(c==2):
        ty=input("Quel profilé voulez-vous soumettre à la compression ?  ")

        return ty

#def Anet(d,q):

def verifTrac(d):
    Ned=int(input("Quelles la valaur de la charge a verifier Ned?  :"))
    A1=d[0][0]*d[0][1]
    A2=d[1][0]*d[1][1]
    match d[0][3]:
        case 1:
            fy1=235
            fu1=360
        case 2:
            fy1=275
            fu1=430
        case 3:
            fy1=355
            fu1=510
    match d[1][3]:
        case 1:
            fy2=235
            fu2=360
        case 2:
            fy2=275
            fu2=430
        case 3:
            fy2=355
            fu2=510
    Npl1=A1*fy1/gamaMo
    Npl2=A2*fy2/gamaMo
    if(d[2][1]<=14):
        phi0=d[2][1]+1
    elif(d[2][1]<=24):
        phi0=d[2][1]+2
    else:
        phi0=d[2][1]+3
    match d[2][2]:
        case 1:
            bn1=d[0][2]-d[2][3]*phi0
            bn2=d[1][2]-d[2][3]*phi0
        case 2:
            bn9=0    
    An1=bn1*d[0][2]
    An2=bn2*d[1][2]
    Nu1=0.9*(An1*fu1/gamaM2)
    Nu2=0.9*(An2*fu2/gamaM2)
    match d[2][4]:
        case 1:
            if(Ned<=Nu1 and Ned<=Npl1):
                print("La premiere plaque resiste bien")
            elif(Ned>Nu1 and Ned<=Npl1):
                print("Il y a ruine fragile au niveau de la plaque 1")
            elif((Ned<=Nu1 and Ned>Npl1)):
                print("Il y a ruine ductile au niveau de la plaque 1")
            else:
                print("Il y a les deux type de ruine dans la premiere plaque")
            
            if(Ned<=Nu2 and Ned<=Npl2):
                print("La deuxième plaque resiste bien")
            elif(Ned>Nu2 and Ned<=Npl2):
                print("Il y a ruine fragile au niveau de la plaque 2")
            elif((Ned<=Nu2 and Ned>Npl2)):
                print("Il y a ruine ductile au niveau de la plaque 2")
            else:
                print("Il y a les deux type de ruine dans la deuxième plaque")
        case 2:
            if(Ned<=Nu1 and Ned<=Npl1):
                print("La premiere plaque resiste bien")
            elif(Ned>Nu1 and Ned<=Npl1):
                print("Il y a ruine fragile au niveau de la plaque 1")
            elif((Ned<=Nu1 and Ned>Npl1)):
                print("Il y a ruine ductile au niveau de la plaque 1")
            else:
                print("Il y a les deux type de ruine dans la premiere plaque")
            
            Ned=Ned/2
            if(Ned<=Nu2 and Ned<=Npl2):
                print("Comme les deux autre sont identiques, nous allons etudier une seule. La deuxième plaque resiste bien")
            elif(Ned>Nu2 and Ned<=Npl2):
                print("Il y a ruine fragile au niveau de la plaque 2")
            elif((Ned<=Nu2 and Ned>Npl2)):
                print("Il y a ruine ductile au niveau de la plaque 2")
            else:
                print("Il y a les deux type de ruine dans la deuxième plaque")
            Ned=Ned*2
        

def verifComp(d,nuance,u,l,alpha):
    #u coefficient en fonction des appui, l=longueur
    match nuance:
        case 1:
            fy1=235
            fu1=360
        case 2:
            fy1=275
            fu1=430
        case 3:
            fy1=355
            fu1=510
    efa=(235/fy1)*0.5
    landa1=93.9*efa
    landa=u*l
    iy=recupData("IPE 100","iy")
    iz=recupData("IPE 100","iz")
    i=iy
    if(i>iz):
        i=iz
    A=recupData("IPE 100","Amm2x102")
    A=A*100
    landa=landa/(i/A)^0.5
    landabar=(landa/landa1)
    if(landabar>=0.2):
        print("Risque de flambement")
    phi=0.5*(1*alpha*(landabar-0.2)+landabar^2)
    si=1/(phi+(phi^2-landabar^2)^0.5)
    Nr=si*A*fy1/gamaM1

def verifCis():
    t=input("Quel type de boulon voulez vous utiliser? ")
    match t:
        case "4.6":
            fyb=240
            fub=400
        case "4.8":
            fyb=320
            fub=400
        case "5.6":
            fyb=300
            fub=500
        case "5.8":
            fyb=400
            fub=500
        case "6.8":
            fyb=480
            fub=600
        case "8.8":
            fyb=640
            fub=800
        case "10.9":
            fyb=900
            fub=1000
    d=int(input("Diamètre du boulon: "))
    if(d<=14):
        phi0=d+1
    elif(d<=24):
        phi0=d+2
    else:
        phi0=d+3
    
    match phi0:
        case 9:
            As=36.6
        case 11:
            As=58
        case 13:
            As=84.3
        case 15:
            As=115
        case 18:
            As=157
        case 20:
            As=192
        case 22:
            As=245
        case 24:
            As=303
        case 26:
            As=353
        case 30:
            As=459
        case 33:
            As=561
    Ab=As
    m= int(input("Combien de plan de cisaillement? "))
    if(t=="4.6" or t=="5.6" or t=="8.8"):
        Fv=m*0.6*fub*Ab/gamaMbc
    else:
        Fv=m*0.5*fub*Ab/gamaMbc
    t=int(input("Epaisseur du plat: "))
    n=int(input("Nuance du plat. Veuillez choisir: \n1. S235\n2. S275\n3. S355"))
    match n:
        case 1:
            fy=235
            fu=360
        case 2:
            fy=275
            fu=430
        case 3:
            fy=355
            fu=510
    p1=int(input("Entrace: "))
    l1=int(input("Largeur du plat: "))
    al=min(l1/(3*phi0),(p1/(3*phi0)-1/4),(fub/fu),1)
    Fb=2.5*al*fu*d*t/gamaMbc
    print("On a Fb= ",Fb,"\nFv= ",Fv)


def Verif(c):
    match c:
        case 1:
            verifTrac()
        case 2:
            verifComp()
        case 3:
            verifCis()
        case _:
            print("Nous rencontrons un probleme au niveau de vos choix. Désolé")
    
def recupData(dez,dd):

    ezliste= ["IPE 1","IPE 2","IPN 1","IPN 2","HE 1","HE 2","UPE 1","UPE 2","UPN 1","UPN 2","L1","L2"]
    #ezl=["p1","p2","p3"]
    #ezdat={}
    for j in ezliste:
        if (dez[0:2]==j[0:2] or dez=="L1" or dez=="L2"):
            base=ezdp.read_excel("BDDP.xlsx",sheet_name=j)
            base = ezdp.DataFrame(base)
            for i in range(len(base["Profile"])):
                if( dez==base["Profile"].iloc[i] ):
                    return base.iloc[i][dd]
                    break
                

                
                    