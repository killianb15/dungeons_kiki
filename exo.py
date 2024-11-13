import random
import numpy as np

ObjetLoot = ["Or", "Arme", "Vie", "Corde", "Rune"]

# Génère la matrice du donjon
def generer_matrice():
    matrice = np.zeros((5, 5), dtype=int)
    for i in range(5):
        for j in range(5):
            matrice[i][j] = random.choice([0, 1])  # 0 = vide, 1 = ennemi
    
    i, j = random.randint(0, 4), random.randint(0, 4)
    matrice[i][j] = 2  # Place un loot aléatoire

    matrice[4][4] = 3  # Place la sortie en bas à droite
    return matrice

# Affiche la matrice du donjon avec la position du joueur
def afficher_matrice(matrice, pos_joueur):
    matrice_affichee = matrice.copy()
    matrice_affichee[pos_joueur] = 8  # Représente la position du joueur
    print(matrice_affichee)

# Fonction de déplacement du joueur
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

# Fouille une salle pour obtenir un loot
def fouillez(inventaire):
    if len(inventaire) < 5: 
        loot = random.choice(ObjetLoot)
        inventaire.append(loot)
        print(f"Vous avez trouvé {loot}!")
    return inventaire

# Compte le nombre d'or dans l'inventaire
def CountOr(inventaire):
    return inventaire.count("Or")

# Vérifie s'il y a 3 runes dans l'inventaire et initie un combat spécial
def combattre_boss(vie, inventaire):
    if inventaire.count("Rune") >= 3:
        print("\nVous avez 3 runes ! Un combat spécial contre le boss commence maintenant !")
        inventaire = [item for item in inventaire if item != "Rune"]  # Enlève les 3 runes de l'inventaire
        
        boss_vie = 3  # Le boss a 3 points de vie
        print("Le boss a 3 points de vie !")
        
        while vie > 0 and boss_vie > 0:  # Le combat dure jusqu'à ce que le joueur ou le boss perde toutes ses vies
            attaque_boss = random.choice(["attaque lourde", "attaque rapide", "essoufflé"])
            
            print(f"\nLe boss prépare une attaque ! {attaque_boss}")
            action_joueur = input("Choisissez votre action : 1 (Roulade), 2 (Protection), 3 (Attaque) : ")
            
            if attaque_boss == "attaque lourde" and action_joueur == '1':
                print("Vous esquivez l'attaque lourde avec une roulade !")
            elif attaque_boss == "attaque rapide" and action_joueur == '2':
                print("Vous bloquez l'attaque rapide avec une protection !")
            elif attaque_boss == "essoufflé" and action_joueur == '3':
                print("Vous attaquez le boss pendant qu'il est essoufflé !")
                boss_vie -= 1  # Le boss perd un point de vie
                print(f"Le boss perd 1 point de vie. Il lui reste {boss_vie} points de vie.")
            else:
                vie -= 1
                print(f"L'action a échoué, vous perdez un point de vie. Vie restante : {vie}")
                
            if vie <= 0:
                print("Vous avez perdu le combat contre le boss.")
                return vie, inventaire, False  # Fin du jeu si le joueur meurt
            
            if boss_vie <= 0:
                print("Vous avez vaincu le boss ! Félicitations !")
                return vie, inventaire, True  # Boss vaincu, retour au jeu

    return vie, inventaire, False


# Interagir avec la salle où le joueur se trouve
def interaction_salle(matrice, pos_joueur, vie, inventaire):
    x, y = pos_joueur
    salle = matrice[x][y]

    if salle == 1:  # Si la salle contient un ennemi
        vie, combat_gagne = combat(vie, inventaire)
        if not combat_gagne:
            print("Vous êtes mort au combat.")
            return vie, inventaire, False  # Fin du jeu si le joueur meurt
    elif salle == 2:  # Si la salle contient un loot
        inventaire = fouillez(inventaire)
        matrice[x][y] = 0  # Vide la salle après le loot
    elif salle == 3:  # Si c'est la sortie
        print("Vous avez atteint la sortie !")
        return vie, inventaire, False  # Fin du niveau, passe au suivant
    return vie, inventaire, True

# Combat avec un ennemi
def combat(vie, inventaire):
    combat_en_cours = True
    while combat_en_cours:
        # Vérifie si l'inventaire contient une arme et si le joueur souhaite l'utiliser
        if "Arme" in inventaire:
            choix_arme = input("Voulez-vous utiliser votre Arme pour gagner immédiatement le combat (oui/non)? ")
            if choix_arme.lower() == "oui":
                print("Vous utilisez votre arme et gagnez immédiatement le combat !")
                inventaire.remove("Arme")
                return vie, True
        
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

# Fonction pour gérer les achats dans le village
def traverse_village(inventaire):
    boutique = input("Voulez-vous acheter un objet avec votre Or (oui ou non)? ")
    if boutique.lower() == "oui": 
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

# Enlever de l'or de l'inventaire
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

# Fonction avant chaque niveau pour gérer les objets de l'inventaire
def utiliser_objets(inventaire, vie):
    if not inventaire:
        print("Votre inventaire est vide. Vous ne pouvez pas utiliser d'objets.")
        return vie, inventaire, True  # On continue le niveau sans demander d'objets
    
    print(f"Inventaire actuel : {inventaire}")
    
    if "Vie" in inventaire:
        choix_vie = input("Voulez-vous utiliser une Vie pour récupérer un point de vie (oui/non)? ")
        if choix_vie.lower() == "oui":
            vie += 1
            inventaire.remove("Vie")
            print(f"Vous avez maintenant {vie} points de vie.")
    
    if "Corde" in inventaire:
        choix_corde = input("Voulez-vous utiliser une Corde pour sortir immédiatement du donjon (oui/non)? ")
        if choix_corde.lower() == "oui":
            print("Vous utilisez la corde pour quitter le donjon immédiatement.")
            inventaire.remove("Corde")
            return vie, inventaire, True  # Sortie du donjon, mais on ne termine pas le jeu
    
    return vie, inventaire, True  # Continue le jeu

# Fonction principale du jeudef 
def main():
    vie = 2
    inventaire = ["Rune", "Rune", "Rune"]
    compteur_dungeons = 0  # Compteur de donjons

    while vie > 0:
        print("\n--- Avant de commencer le niveau, choisissez vos objets ---")
        vie, inventaire, continuer = utiliser_objets(inventaire, vie)
        if not continuer:
            print("Vous avez quitté le donjon avec succès.")
            break

        # Générer un nouveau niveau
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
                    print("🪙 Vous n'avez pas assez d'Or pour visiter la boutique. 🪙")
                    print(f"Votre inventaire à la fin du donjon : {inventaire}")
                compteur_dungeons += 1  # Incrementer le compteur des donjons
                break  # Passe au niveau suivant

        # Après avoir quitté le donjon et visité le village
        vie, inventaire, boss_combat = combattre_boss(vie, inventaire)
        
        if boss_combat:
            print("Vous avez battu le boss final, mais le jeu continue !")
            # Vous pouvez ajouter une logique pour continuer à explorer d'autres niveaux ou boucles ici
            continue  # Continue la boucle principale sans sortir du jeu, après avoir vaincu le boss

    print(f"☠️ Vous avez perdu toutes vos vies. Fin de la partie. ☠️")
    print(f"Nombre de donjons terminés : {compteur_dungeons}")

main()
