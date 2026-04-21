import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QFileDialog,
    QLabel, QLineEdit,QInputDialog
)

from traitement_csv import (
    lire_fichier, gen_donnees,
    abr_prix, parcoursInfixe,
    couts_payes, recette_vendeur, gagnant, lire_multimanche_fusion
)


class Fenetre(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enchère LowBid")
        self.resize(500, 500)

        self.layout = QVBoxLayout()

        self.label = QLabel("Résultats :")
        self.layout.addWidget(self.label)

        # on peut modifier le alpha !!
        self.label_alpha = QLabel("Alpha :")
        self.layout.addWidget(self.label_alpha)

        self.input_alpha = QLineEdit()
        self.input_alpha.setText("10")  # valeur par défaut
        self.layout.addWidget(self.input_alpha)

        self.zone = QTextEdit()
        self.layout.addWidget(self.zone)

        # boutons
        self.btn_gen = QPushButton("Générer données")
        self.btn_gen.clicked.connect(self.generer)
        self.layout.addWidget(self.btn_gen)

        self.btn_csv = QPushButton("Charger CSV")
        self.btn_csv.clicked.connect(self.charger_csv)
        self.layout.addWidget(self.btn_csv)

        self.btn_calc = QPushButton("Calculer enchère")
        self.btn_calc.clicked.connect(self.calculer)
        self.layout.addWidget(self.btn_calc)

        self.setLayout(self.layout)

        self.data = []

    # ------------------------

    def generer(self):
        self.data = gen_donnees(10)
        self.zone.setText("Données générées !")

    def charger_csv(self):
        options = [
            "Démo (10 joueurs)",
            "Multi-manches (500x40)",
            "Stress test (200k)"
        ]

        choix, ok = QInputDialog.getItem(
            self,
            "Choisir un fichier",
            "Sélectionne un jeu de données :",
            options,
            0,
            False
        )

        if ok:
            if choix == options[0]:
                self.data = lire_fichier("data/lowbid_manche_demo.csv")
            elif choix == options[1]:
                self.data = lire_multimanche_fusion()
            else:
                self.data = lire_fichier("data/lowbid_stress_200k.csv")
            
            self.zone.setText(f"Fichier chargé : {choix}")

    def calculer(self):
        if not self.data:
            self.zone.setText("Aucune donnée !")
            return

        # récupérer alpha
        try:
            alpha = float(self.input_alpha.text())
        except:
            self.zone.setText("Alpha invalide !")
            return

        abr = abr_prix(self.data)

        texte = ""

        # affichage enchère
        for prix, joueurs in parcoursInfixe(abr):
            cout = 1 + alpha / (prix + 1)
            texte += f"Prix : {prix} | Joueurs : {joueurs} | Coût : {cout:.2f}\n"

        # gagnant
        g = gagnant(abr)
        if g:
            texte += f"\n Gagnant : {g[0]} avec le prix {g[1]}"
        else:
            texte += "\n Aucun gagnant (pas de prix unique!)"

        # coûts
        texte += "\n\nCoûts joueurs :\n"
        couts = couts_payes(abr, 1, alpha)
        for j, c in couts.items():
            texte += f"{j} : {c:.2f}\n"

        # recette
        recette = recette_vendeur(abr, 1, alpha)
        texte += f"\nRecette vendeur : {recette:.2f}"

        self.zone.setText(texte)


# ------------------------

app = QApplication(sys.argv)
fen = Fenetre()
fen.show()
sys.exit(app.exec_())