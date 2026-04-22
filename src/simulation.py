import random
from traitement_csv import Noeud


def calculer_recette_manche(noeud_actuel, cout_base, alpha):
    """ Calcule la somme de toutes les mises selon la formule du sujet """
    if noeud_actuel is None:
        return 0


    """ formule cout = cout_base + (alpha / (prix+1)) """
    nb_joueurs_ici = len(noeud_actuel.joueurs)
    cout_unitaire = cout_base + (alpha / (noeud_actuel.prix + 1))
    recette_noeud = nb_joueurs_ici * cout_unitaire

    """ on additionne recursivement tout l'arbre """
    return (recette_noeud + 
            calculer_recette_manche(noeud_actuel.gauche, cout_base, alpha) + 
            calculer_recette_manche(noeud_actuel.droite, cout_base, alpha))


def trouver_gagnant_unique(noeud_actuel):
    """ 
    Parcours infixe pour trouver le plus petit prix 
    qui n'a qu'un seul joueur dans sa liste.
    """
    if noeud_actuel is None:
        return None

    """ on cherche le gagnant dans les prix les plus bas """
    gagnant_gauche = trouver_gagnant_unique(noeud_actuel.gauche)
    if gagnant_gauche:
        return gagnant_gauche
    
    if len(noeud_actuel.joueurs) == 1:
        return noeud_actuel
    """ noeud_actuel c'est notre gagnant """
        
    return trouver_gagnant_unique(noeud_actuel.droite)


def inserer_noeud(racine, prix, joueur):
    if racine is None:
        return Noeud(prix, joueur)
    
    if prix == racine.prix:
        racine.joueurs.append(joueur)
    elif prix < racine.prix:
        racine.gauche = inserer_noeud(racine.gauche, prix, joueur)
    else:
        racine.droite = inserer_noeud(racine.droite, prix, joueur)
    return racine


def simuler_500_manches():
    joueurs = {
        "Bot_Aleatoire": "random",
        "Bot_Prudent": "safe",
        "Bot_Agressif": "low"
    }
    
    stats_victoires = {nom: 0 for nom in joueurs}
    stats_victoires["PERSONNE"] = 0
    recette_totale = 0
    
    for i in range(500):
        racine_manche = None
        
        """ chaque bot joue selon sa logique """
        for nom, strategie in joueurs.items():
            if strategie == "random":
                prix = random.randint(0, 50)
            elif strategie == "safe":
                prix = random.randint(10, 25)
            else: # low
                prix = random.randint(0, 5)
            
            """ on insere la manche dans l'arbre"""
            racine_manche = inserer_noeud(racine_manche, prix, nom)
        
        """ on analyse la manche """
        gagnant = trouver_gagnant_unique(racine_manche)
        recette_totale += calculer_recette_manche(racine_manche, 1.0, 10.0)
        
        if gagnant:
            stats_victoires[gagnant.joueurs[0]] += 1
        else:
            stats_victoires["PERSONNE"] += 1

    """on affiche les resultats """
    print("--- RESULTATS DES 500 MANCHES ---")
    for nom, score in stats_victoires.items():
        print(f"{nom} : {score} victoires")
    print(f"Recette moyenne par manche : {recette_totale / 500:.2f}€")

""" on lance la simulation """
simuler_500_manches()