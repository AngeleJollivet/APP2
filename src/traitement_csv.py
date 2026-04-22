import csv
import random

DEMO = "data\lowbid_manche_demo.csv"
MULTIMANCHES = "data\lowbid_multi_manches_500x40.csv"
STRESS = "data\lowbid_stress_200k.csv"

#------------- FONCTIONS DE LECTURE DU CSV !!!!!!!!!!------------

def lire_fichier(fichier):
    '''lit un fichier csv et retourne une liste de dictionnaires
    Args:
        fichier (str): le nom d'un des deux fichiers à manche unique, DEMO et STRESS
    Returns:
        liste : une liste de dictionnaires associant le joueur à sa mise.
    '''
    liste = []
    with open(fichier, newline='') as f : 
        reader = csv.reader(f,delimiter=',')
        next(reader) # on skip la ligne 1
        for row in reader : 
            l = []
            for value in row :
                l.append(value)
            dic = {}
            dic[l[0]] = int(l[1])
            liste.append(dic)
    #liste = liste[1:]
    return liste

def lire_multimanche_fusion(): # on perd totalement le concept de manches cela dit donc c'est pas optimal mais c'est simple et efficace
    '''lit un fichier csv multimanche

    Returns:
        liste : une liste de dictionnaires associant le joueur à sa mise.
        on fusionne toutes les manches en une.
    '''
    liste = []

    with open(MULTIMANCHES, newline='') as f:
        reader = csv.reader(f, delimiter=',')

        next(reader)  # on se débarrasse de l'en-tête

        for row in reader:
            joueur = row[1]
            prix = int(row[2])

            liste.append({joueur: prix})

    return liste

def lire_multimanche(): #la on conserve le concepot de manche mais ça implique demanipuler toutes les autres fonctions 
    donnees = {} #dictionnaire de liste de dictionnaires

    with open(MULTIMANCHES, newline='') as f:
        reader = csv.reader(f, delimiter=',')

        next(reader)  # saute l'en-tête

        for row in reader:
            manche = int(row[0])
            joueur = row[1]
            prix = int(row[2])
            if manche not in donnees:
                donnees[manche] = []
            donnees[manche].append({joueur: prix})

    return donnees

def gen_donnees(n):
    ''' Génère une liste de n données
    Args :
        n (int) : le nombre de données qu'on veut générer
    Returns : 
        liste : une liste de dictionnaire avec des joueurs associés à des nombre aléatoire 
    '''
    liste = []
    #L_noms = []
    #L_prix = []
    for i in range(n):
        dic = {}
        #L_noms.append("J"+ str(n))
        #L_prix.append(random.randint(0,200))
        dic["J"+str(i)] = random.randint(0,200)
        liste.append(dic)
    return liste


#------------------FONCTIONS SUR LES ARBRES !!!!!!! -------------------------------

class Noeud:
    def __init__(self, prix, joueur):
        self.prix = prix
        self.joueurs = [joueur] # ils sont dans une liste pour pouvoir associer plusieurs joueurs au même prix
        self.gauche = None
        self.droite = None


def inserer(racine, dic_joueur_prix):
    ''' insère les noeuds prix/joueurs dans un abr
    Args :
        racine (Noeud) : la racine de l'abr ou l'on souhaite insérer le noeud
        dic_joueur_prix (dictionnaire) : le dictionnaire au format {joueur : prix}
    Returns : 
        racine (Noeud): la racine mise à jour
    '''
    for joueur, prix in dic_joueur_prix.items():

        # arbre vide
        if racine is None:
            return Noeud(prix, joueur)

        # si le prix ets le même, on ajoute le joueur au  noeud
        if prix == racine.prix:
            racine.joueurs.append(joueur)

        elif prix < racine.prix:
            racine.gauche = inserer(racine.gauche, dic_joueur_prix)

        else:
            racine.droite = inserer(racine.droite, dic_joueur_prix)

    return racine

def trouver_successeur(racine, prix_cible):
    ''' 
    Trouve le nœud avec le plus petit prix strictement supérieur au prix_cible.
    Utile pour trouver le prochain candidat si le prix le plus bas n'est pas unique.
    '''
    successeur_potentiel = None
    courant = racine

    while courant is not None:
        if courant.prix > prix_cible:
            successeur_potentiel = courant
            courant = courant.gauche
        else:
            courant = courant.droite

    return successeur_potentiel

def trouver_predecesseur(racine, prix_cible):
    ''' 
    Trouve le nœud avec le plus grand prix strictement inférieur au prix_cible.
    '''
    predecesseur_potentiel = None
    courant = racine

    while courant is not None:
        if courant.prix < prix_cible:
            predecesseur_potentiel = courant
            courant = courant.droite
        else:
            courant = courant.gauche

    return predecesseur_potentiel


def abr_prix(liste):
    ''' Pour former l'arbre en fonction des prix
    Args :
        liste (list) : une liste de dictionnaire avec les joueurs et leur mise
    Returns : 
        abr : un arbre binaire de recherche tel que les mises consistent les noeuds.
        Si un prix a été misé plusieurs fois, les joueurs seront regroupés dans la même liste
    '''
    abr = None
    for val in liste : 
        abr = inserer(abr,val)
    return abr

def parcoursInfixe(abr):
    ''' pour parcourir l'abr en parcours infixe
    Args :
        abr (arbre binaire de recherche) : l'arbre binaire de recherche joueurs/prix
    Returns : 
        liste : renvoie la liste des noeuds joueurs/prix, de la plus petite mise à la plus grande
        au format prix,joueur
    '''
    if abr is None:
        return []
    
    return (parcoursInfixe(abr.gauche) + [(abr.prix, abr.joueurs)] + parcoursInfixe(abr.droite))


def afficher_Enchere(abr, cout_base=1, alpha=10):
    ''' on affiche l'état de l'enchère de la plus petite mise à la plus grande
    Args :
        abr (arbre binaire de recherche) : l'arbre binaire de recherche joueurs/prix
        cout_base (int) : un cout de réference, par défaut nous avons choisi 1€
        alpha (int) : paramètre d'intensité de la prime de risque, par défaut nous avons choisi 10
    Returns : 
        affiche dans le terminal le mise, les joueurs associés, et le coût payé par les joueurs pour effectuer cette mise
    '''   
    liste = parcoursInfixe(abr)

    for prix, joueurs in liste:
        cout = cout_base + alpha / (prix + 1)
        print("Prix :", prix,"-> Joueurs :", joueurs,"| Coût :", f"{cout:.2f}") # la aussi j'arrondit à 2cs


def couts_payes(abr, cout_base=1, alpha=10):
    ''' créer un dictionnaire associant les joueur au coût de leur mise
    Args :
        abr (arbre binaire de recherche) : l'arbre binaire de recherche joueurs/prix
        cout_base (int) : un cout de réference, par défaut nous avons choisi 1€
        alpha (int) : paramètre d'intensité de la prime de risque, par défaut nous avons choisi 10
    Returns : 
        couts : dictionnaire au format {joueur : cout de sa mise}
    '''
    liste = parcoursInfixe(abr)
    couts = {}

    for prix, joueurs in liste:
        cout = round(cout_base + alpha / (prix + 1), 2) # ici on arrondit à deux chiffres après la virgule

        for j in joueurs:
            couts[j] = cout

    return couts

def recette_vendeur(abr, cout_base=1, alpha=10): # on choisit un alpha a 10 pour voir une vrai différence dans les couts, on pourrait tester avec 100 why not ?
    ''' calcule le bénéfice du vendeur à la fin de l'enchère
    Args :
        abr (arbre binaire de recherche) : l'arbre binaire de recherche joueurs/prix
        cout_base (int) : un cout de réference, par défaut nous avons choisi 1€
        alpha (int) : paramètre d'intensité de la prime de risque, par défaut nous avons choisi 10
    Returns : 
        sum(couts.values()) : somme de tous les coûts de chaque mise des joueurs afin de détérminer la recette du vendeur
    '''   
    couts = couts_payes(abr, cout_base, alpha)
    return sum(couts.values())

def gagnant(abr):
    ''' on détermine le gagnant de l'enchère
    Args : 
        abr (arbre binaire de recherche) : l'arbre binaire de recherche joueurs/prix 
    Returns :
        renvoit le joueur et sa mise de la plus petite mise unique si elle existe, sinon None'''
    for prix, joueurs in parcoursInfixe(abr): # on prend le dictionnaire prix/joueur du parcours infixe
        if len(joueurs) == 1: # si la  liste des joueurs n'en contient qu'un seul (mise unique)
            return joueurs[0], prix # alors il gagne, on retourne le joueur et sa mise
    return None


def trouver_min(noeud):
    """
    Parcourt l'arbre vers la gauche pour trouver le noeud ayant le prix le plus bas.
    
    Args:
        noeud (Noeud): Le point de départ de la recherche.
        
    Returns:
        Noeud: Le noeud contenant le prix minimum dans ce sous-arbre.
    """
    courant = noeud
    while courant.gauche is not None:
        courant = courant.gauche
    return courant

def supprimer_mise(racine, prix, nom_joueur):
    """
    Supprime la mise d'un joueur spécifique pour un prix donné. 
    Si le joueur était le seul sur ce prix, le noeud est supprimé de l'ABR
    tout en conservant la structure de recherche.
    
    Args:
        racine (Noeud): La racine actuelle de l'arbre (ou sous-arbre).
        prix (int): Le prix de la mise à supprimer.
        nom_joueur (str): Le nom du joueur qui retire sa mise.
        
    Returns:
        Noeud: La nouvelle racine du sous-arbre après suppression.
    """
    if racine is None:
        return None

    # Recherche du noeud à traiter
    if prix < racine.prix:
        racine.gauche = supprimer_mise(racine.gauche, prix, nom_joueur)
    elif prix > racine.prix:
        racine.droite = supprimer_mise(racine.droite, prix, nom_joueur)
    else:
        # Le prix est trouvé, on retire le joueur de la liste
        if nom_joueur in racine.joueurs:
            racine.joueurs.remove(nom_joueur)
        
        # Si d'autres joueurs ont misé ce prix, on s'arrête là
        if len(racine.joueurs) > 0:
            return racine
        
        # Sinon, suppression physique du noeud (Cas ABR classique)
        # Cas 1 & 2 : Le noeud a 0 ou 1 enfant
        if racine.gauche is None:
            return racine.droite
        elif racine.droite is None:
            return racine.gauche
        
        # Cas 3 : Le noeud a 2 enfants
        # On remplace par le successeur (le min du sous-arbre droit)
        temp = trouver_min(racine.droite)
        racine.prix = temp.prix
        racine.joueurs = temp.joueurs
        # On supprime le noeud qui a été déplacé
        racine.droite = supprimer_mise(racine.droite, temp.prix, temp.joueurs[0])
        
    return racine

def trouver_successeur(racine, prix_cible):
    """
    Identifie le noeud ayant le plus petit prix strictement supérieur au prix cible.
    
    Args:
        racine (Noeud): La racine de l'ABR.
        prix_cible (int): Le prix de référence.
        
    Returns:
        Noeud: Le successeur trouvé ou None s'il n'existe pas.
    """
    successeur_potentiel = None
    courant = racine

    while courant is not None:
        if courant.prix > prix_cible:
            successeur_potentiel = courant
            courant = courant.gauche
        else:
            courant = courant.droite

    return successeur_potentiel


#-----------Tests : ----------------------------------
data = gen_donnees(10)
abr = abr_prix(data)

#print(abr_prix(gen_donnees(10)))

afficher_Enchere(abr)

print("Coûts :", couts_payes(abr))
print("Recette :", recette_vendeur(abr))