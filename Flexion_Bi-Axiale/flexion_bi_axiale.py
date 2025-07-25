# fonction qui affiche le menu pour savoir ce que veut faire l'utilisateur
def affiche():

    print("Bienvenu dans le programme FLEXION BI-AXIALE!\nIl s'agit de profil simple en I ou H à semelles égales, soumis à des moments\nuniformes"
          " avec ou sans contrainte normale uniformement répartie"
           " et comportant \ndes maintiens d'extrémité simples,surtout les IPE et HE.\n"
          "Que voulez vous faire?:\n"
          "1-Une Vérification,\n2-Un dimensionnement,\n3-Obtenir les valeurs maximales des charges que peut supporter votre section")
    
    choix = input("Veuillez entrez 1 ou 2 ou encore 3 selon votre choix: ")
    return choix

# veuiller à ce que l'utilsateur fasse un choix correct
while True:

    try:
        choix = int(affiche())
        if choix != 1 and choix != 2 and choix != 3:
            raise ValueError()
        break
    except ValueError:
        print("Erreur:vous n'avez pas entré 1,2 ou 3")

# exécution du choix

if choix == 1:

    print("__Commencement de la vérification!__\n")
    from vérification import verification
    verification()
    print("Fin de la vérification.")

elif choix == 2:

    print("__Alors on commence le dimensionnement!__\n")
    import dimensionnement
    print("FIN.Au revoir!")

elif choix == 3:

    print("__Recherche de charges maximales__\n")
    from charges_maxi import max_charges
    max_charges()
    print("FIN!")
    