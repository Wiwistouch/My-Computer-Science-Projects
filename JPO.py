from matplotlib import pyplot as plt
from random import randrange

# ---------------- Directions ---------------- #
Direction = {
    "E": {"ligne": 0, "colonne": 1, "associee": "O"},
    "S": {"ligne": 1, "colonne": 0, "associee": "N"},
    "O": {"ligne": 0, "colonne": -1, "associee": "E"},
    "N": {"ligne": -1, "colonne": 0, "associee": "S"},
}

# ---------------- Case ---------------- #
class Case():
    def __init__(self):
        self.murs = {"N": True, "E": True, "S": True, "O": True}
        self.identifiant = 0
        self.visite = False

    def set_murs(self, direction, etat):
        self.murs[direction] = etat

    def get_murs(self):
        return self.murs

    def set_identifiant(self, id):
        self.identifiant = id

    def get_identifiant(self):
        return self.identifiant

# ---------------- Grille ---------------- #
class Grille():
    def __init__(self, hauteur, largeur):
        self.plateau = [[Case() for _ in range(largeur)] for _ in range(hauteur)]
        self.chemin = []

    def get_hauteur(self):
        return len(self.plateau)

    def get_largeur(self):
        return len(self.plateau[0])

    def get_case(self, ligne, colonne):
        return self.plateau[ligne][colonne]

    def voisine(self, ligne, colonne, direction):
        ligne_vois = ligne + Direction[direction]["ligne"]
        colonne_vois = colonne + Direction[direction]["colonne"]
        return self.get_case(ligne_vois, colonne_vois)

    def init_identifiants(self):
        for ligne in range(self.get_hauteur()):
            for colonne in range(self.get_largeur()):
                ident = ligne * self.get_largeur() + colonne
                self.plateau[ligne][colonne].set_identifiant(ident)

    def get_identifiant(self, ligne, colonne):
        return self.get_case(ligne, colonne).get_identifiant()

    def set_identifiant(self, ligne, colonne, id):
        self.get_case(ligne, colonne).set_identifiant(id)

    def murs_cassables(self, ligne, colonne):
        largeur = self.get_largeur()
        hauteur = self.get_hauteur()
        case = self.get_case(ligne, colonne)
        murs_case = case.murs
        id_1 = case.get_identifiant()
        directions_interdites = []

        if ligne == 0 or self.get_identifiant(ligne-1, colonne) == id_1:
            directions_interdites.append("N")
        if colonne == 0 or self.get_identifiant(ligne, colonne-1) == id_1:
            directions_interdites.append("O")
        if ligne == hauteur-1 or self.get_identifiant(ligne+1, colonne) == id_1:
            directions_interdites.append("S")
        if colonne == largeur-1 or self.get_identifiant(ligne, colonne+1) == id_1:
            directions_interdites.append("E")

        return [direction for direction in murs_case if direction not in directions_interdites]

    def unifier_identifiants(self, id_1, id_2):
        for i in range(self.get_hauteur()):
            for j in range(self.get_largeur()):
                if self.get_identifiant(i,j) == id_2:
                    self.set_identifiant(i,j,id_1)

    def detruit_mur(self, ligne, colonne, direction):
        case = self.get_case(ligne, colonne)
        id_1 = case.get_identifiant()
        case.set_murs(direction, False)

        ligne_vois = ligne + Direction[direction]["ligne"]
        colonne_vois = colonne + Direction[direction]["colonne"]
        case_vois = self.get_case(ligne_vois, colonne_vois)

        id_2 = case_vois.get_identifiant()
        case_vois.set_murs(Direction[direction]["associee"], False)
        self.unifier_identifiants(id_1, id_2)

    def generer_labyrinthe(self):
        hauteur = self.get_hauteur()
        largeur = self.get_largeur()
        self.init_identifiants()
        nombre_identifiants = hauteur * largeur

        while nombre_identifiants > 1:
            ligne = randrange(hauteur)
            colonne = randrange(largeur)
            murs = self.murs_cassables(ligne, colonne)

            if murs:
                direction = murs[randrange(len(murs))]
                self.detruit_mur(ligne, colonne, direction)
                nombre_identifiants -= 1

    def solution(self, ligne_0, colonne_0, ligne_1, colonne_1):
        case = self.get_case(ligne_0, colonne_0)
        case.visite = True
        self.chemin.append((ligne_0, colonne_0))

        if (ligne_0, colonne_0) == (ligne_1, colonne_1):
            return self.chemin.copy()

        for direction in ["N", "E", "S", "O"]:
            if not case.murs[direction]:
                ligne_vois = ligne_0 + Direction[direction]["ligne"]
                colonne_vois = colonne_0 + Direction[direction]["colonne"]

                if 0 <= ligne_vois < self.get_hauteur() and 0 <= colonne_vois < self.get_largeur():
                    if not self.get_case(ligne_vois, colonne_vois).visite:
                        resultat = self.solution(ligne_vois, colonne_vois, ligne_1, colonne_1)
                        if resultat:
                            return resultat

        self.chemin.pop()
        return []

    # ---------------- Dessin stylisé ---------------- #
    def dessine(self, chemin, deb, fin):
        THICKNESS_WALL = 1.5
        THICKNESS_PATH = 3.0
        largeur = self.get_largeur()
        hauteur = self.get_hauteur()
        
        plt.figure(figsize=(largeur/2, hauteur/2))
        plt.axis("off")
        plt.gca().set_facecolor("#f0f0f0")  # fond gris clair

        # Draw start (green) and end (red)
        plt.fill([deb[1], deb[1]+1, deb[1]+1, deb[1]], 
                 [hauteur-deb[0]-1, hauteur-deb[0]-1, hauteur-deb[0], hauteur-deb[0]], color="green")
        plt.fill([fin[1], fin[1]+1, fin[1]+1, fin[1]], 
                 [hauteur-fin[0]-1, hauteur-fin[0]-1, hauteur-fin[0], hauteur-fin[0]], color="red")

        # Draw outer border
        plt.plot([0, largeur, largeur, 0, 0],
                 [0, 0, hauteur, hauteur, 0],
                 linewidth=THICKNESS_WALL, color='black')

        # Draw walls
        for ligne in range(hauteur):
            for colonne in range(largeur):
                case = self.get_case(ligne, colonne)
                if case.murs["N"]:
                    plt.plot([colonne, colonne + 1],
                             [hauteur - ligne, hauteur - ligne],
                             linewidth=THICKNESS_WALL, color='black')
                if case.murs["E"]:
                    plt.plot([colonne + 1, colonne + 1],
                             [hauteur - ligne - 1, hauteur - ligne],
                             linewidth=THICKNESS_WALL, color='black')

        # Draw solution path with rounded corners
        for i in range(1, len(chemin)):
            l0, c0 = chemin[i - 1]
            l1, c1 = chemin[i]
            plt.plot((c0 + 0.5, c1 + 0.5),
                     (hauteur - l0 - 0.5, hauteur - l1 - 0.5),
                     color='red', linewidth=THICKNESS_PATH, solid_capstyle='round')

        plt.show()

# ---------------- Interactive loop ---------------- #
print("\n=== Bienvenue dans le générateur de labyrinthe ! ===")
print("Tapez /help pour voir toutes les commandes disponibles.\n")

while True:
    commande = input("Commande : ").strip()

    if commande == "/help":
        print("\n--- Commandes disponibles ---")
        print("  /help          -> Afficher ce message d'aide")
        print("  quit, /q, q    -> Quitter le programme")
        print("  /start pour lancer la creation d'un labyrinthe\n")
        
    elif commande in ["quit", "/q", "q", "exit"]:
        print("\nAu revoir !\n")
        break

    elif commande == "/start":
        print("  Pour générer un labyrinthe :")
        print("    taille : h,l     (ex : 20,20)")
        print("    debut : ligne,col (ex : 0,0)")
        print("    fin   : ligne,col (ex : 19,19)\n")

        try:
            taille = input("Taille (hauteur,largeur) : ").split(",")
            debut = input("Point de départ (ligne,colonne) : ").split(",")
            fin = input("Point d'arrivée (ligne,colonne) : ").split(",")

            hauteur, largeur = int(taille[0]), int(taille[1])
            ligne_deb, col_deb = int(debut[0]), int(debut[1])
            ligne_fin, col_fin = int(fin[0]), int(fin[1])

            labyrinthe = Grille(hauteur, largeur)
            print("\nGénération du labyrinthe...")
            labyrinthe.generer_labyrinthe()
            print("Labyrinthe généré avec succès !")

            print("Recherche du chemin...")
            chemin = labyrinthe.solution(ligne_deb, col_deb, ligne_fin, col_fin)
            if chemin:
                print(f"Chemin trouvé : {len(chemin)} étapes.\n")
            else:
                print("Aucun chemin trouvé !\n")

            print("merci de fermer la fenetre pour recomencer ou si vous avez fini \n")

            labyrinthe.dessine(chemin, (ligne_deb, col_deb), (ligne_fin, col_fin))

        except Exception as e:
            print("\nErreur :", e)
            print("Assurez-vous d'entrer des valeurs valides. Exemple : 20,20 ou 0,0\n")
