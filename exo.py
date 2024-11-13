import random
import numpy as np

#hugo thouin-dugand
#killian bouhourd


ObjetLoot = ["Or", "Arme", "Vie", "Corde", "Rune"]
#ObjetLoot = ["Or"]
def generer_matrice():
    matrice = np.zeros((5, 5), dtype=int)
    for i in range(5):
        for j in range(5):
            matrice[i][j] = random.choice([0, 1])  # 0 = vide, 1 = ennemi
    
    i, j = random.randint(0, 4), random.randint(0, 4)
    matrice[i][j] = 2  # Place un loot aléatoire

    matrice[4][4] = 3  # Place la sortie en bas à droite
    return matrice

def afficher_matrice(matrice, pos_joueur):
    matrice_affichee = matrice.copy()
    matrice_affichee[pos_joueur] = 8  # Représente la position du joueur
    print(matrice_affichee)

def deplacement(pos_joueur, direction):
    x, y = pos_joueur
    if direction == 'z' and x > 0:
        x -= 1
    elif direction == 's' and x < 4:
        x += 1
    elif direction == 'q' and y > 0:
        y -= 1
    elif direction == 'd' and y < 4:
        y += 1
    return (x, y)

def fouillez(inventaire):
    if len(inventaire) < 5: 
        loot = random.choice(ObjetLoot)
        inventaire.append(loot)
        print(f"Vous avez trouvé {loot}!")
    return inventaire

def CountOr(inventaire):
    return inventaire.count("Or")

def interaction_salle(matrice, pos_joueur, vie, inventaire):
    x, y = pos_joueur
    salle = matrice[x][y]
    if salle == 1:
        vie, combat_gagne = combat(vie)
        if not combat_gagne:
            print("Vous êtes mort au combat.")
            return vie, inventaire, False  # Fin du jeu si le joueur meurt
    elif salle == 2:
        inventaire = fouillez(inventaire)
        matrice[x][y] = 0  # Vide la salle après le loot
    elif salle == 3:
        print("Vous avez atteint la sortie !")
        return vie, inventaire, False  # Fin du niveau, passe au suivant
    return vie, inventaire, True

def combat(vie):
    combat_en_cours = True
    while combat_en_cours:
        resultat_de = random.randint(1, 2)
        print(f"Action de l'ennemi : {resultat_de}")
        action_joueur = input("Voulez-vous vous protéger ou attaquer (1 ou 2)? ")
        
        while action_joueur not in ['1', '2']:
            action_joueur = input("Entrée invalide. Voulez-vous vous protéger ou attaquer (1 ou 2)? ")
        
        if resultat_de == 2 and action_joueur == '2':
            vie -= 1
            print("Vous avez perdu un point de vie.")
            if vie <= 0:
                return vie, False
        elif resultat_de == 1 and action_joueur == '2':
            print("Vous avez gagné le combat !")
            combat_en_cours = False
        elif resultat_de == 2 and action_joueur == '1':
            print("L'ennemi attaque mais vous vous protégez.")
        elif resultat_de == 1 and action_joueur == '1':
            print("L'ennemi ne fait rien, rien ne se passe")
            
    return vie, True

def traverse_village(inventaire):
    boutique = input("Voulez-vous acheter un objet avec votre Or (oui ou non)? ")
    if boutique.lower() == "oui": #tout mettre en minuscule pour accepté les OUI Oui  
        choix = input("1 d'or et je vous donne un objet magnifique (oui ou non) ")
        if choix.lower() == "oui" and CountOr(inventaire) >= 1:
            inventaire = enlever_or(inventaire, 1)
            inventaire = fouillez(inventaire)
            print(f"Voici votre inventaire après cet achat : {inventaire}")
        else:
            print("Vous n'avez pas assez d'Or.")
    else:
        print("Vous quittez le village.")
    return inventaire

def enlever_or(inventaire, quantite):
    or_enleve = 0
    while "Or" in inventaire and or_enleve < quantite:
        inventaire.remove("Or")
        or_enleve += 1
    
    if or_enleve > 0:
        print(f"{or_enleve} Or a été retiré de votre inventaire.")
    else:
        print("Vous n'avez pas assez d'Or.")
    
    return inventaire

def main():
    vie = 2
    inventaire = []
    
    # La boucle continue tant que le joueur a des points de vie
    while vie > 0:
        matrice = generer_matrice()
        pos_joueur = (0, 0)
        succes = True
        
        print("\nNouveau niveau généré.")
        while succes:
            afficher_matrice(matrice, pos_joueur)
            direction = input("Déplacez-vous avec z (haut), s (bas), q (gauche), d (droite) : ")
            nouvelle_position = deplacement(pos_joueur, direction)
            
            if nouvelle_position == pos_joueur:
                print("Déplacement invalide. Réessayez.")
                continue
            
            pos_joueur = nouvelle_position
            vie, inventaire, succes = interaction_salle(matrice, pos_joueur, vie, inventaire)
            
            if not succes and matrice[pos_joueur] == 3:  # Atteint la sortie
                print("Vous avez terminé le niveau avec succès !")
                if CountOr(inventaire) > 0:
                    inventaire = traverse_village(inventaire)
                else:
                    print("🪙  Vous n'avez pas assez d'Or pour visiter la boutique. 🪙")
                    print(f"Votre inventaire à la fin du dungeons : {inventaire}")
                break  # Passe au niveau suivant
        
    print(f"☠️  Vous avez perdu toutes vos vies. Fin de la partie. ☠️")

# Lancer le jeu
main()
