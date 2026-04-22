from traitement_csv import Noeud
from simulation import simuler_500_manches, jouer_une_manche 

def menu():
    """ Affiche un menu interactif dans la console """
    print("\n" + "="*30)
    print("   BIENVENUE CHEZ LOWBID")
    print("="*30)
    print("1. Lancer une simulation (500 manches)")
    print("2. Jouer une manche rapide (Bots uniquement)")
    print("3. Quitter")
    
    choix = input("\nChoisissez une option : ")
    return choix

if __name__ == "__main__":
    continuer = True
    
    while continuer:
        option = menu()
        
        if option == "1":
            print("\n--- Lancement de la simulation massive ---")
            simuler_500_manches()
            
        elif option == "2":
            print("\n--- Simulation d'une seule manche ---")
            joueurs = ["Alice", "Bob", "Charlie", "David"]
            res = jouer_une_manche(joueurs)
            
            print(f"Gagnant : {res['nom_gagnant']}")
            print(f"Prix : {res['prix_gagnant']}")
            print(f"Recette vendeur : {res['recette_vendeur']:.2f}€")
            
        elif option == "3":
            print("Au revoir !")
            continuer = False
        else:
            print("Option invalide, réessayez.")