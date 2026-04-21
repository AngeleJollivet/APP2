import csv

DEMO = "data\lowbid_manche_demo.csv"
MULTIMANCHES = "data\lowbid_multi_manches_500x40.csv"
STRESS = "data\lowbid_stress_200k.csv"

#lecture des fichiers cvs

def lire_fichier(fichier):
    liste = []
    with open(fichier, newline='') as f :
        reader = csv.reader(f,delimiter=',')
        for row in reader :
            l = []
            for value in row :
                l.append(value)
            dic = {}
            dic[l[0]] = l[1]
            liste.append(dic)
    liste = liste[1:]
    return liste

lire_fichier(DEMO)

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#recherche_prix_gagnant() => valeur minimale de l'ABR

def parcoursInfixe(arbre):
    if len(arbre) == 0:
        return []
    if len(arbre) == 1:
        return [arbre[0]]
    gauche = arbre[1] if len(arbre) > 1 else []
    droite = arbre[2] if len(arbre) > 2 else []
    return parcoursInfixe(gauche) + [arbre[0]] + parcoursInfixe(droite)

#retourne la valeur minimale de l'arbre => valeur gagnante

def min_value_victoire(racine):
    if racine is None:
        raise ValueError("L'arbre est vide")

    current = racine
    while current.left is not None:
        current = current.left
    return current.val

