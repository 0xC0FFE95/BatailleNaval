from tkinter import *

class Navire:
    """
    Représente un navire avec un nom, une taille,
    ses positions (liste de tuples de coordonnées),
    et un état (touché ou coulé).
    """
    # Liste de tuples pour chaque navire : (nom, taille)
    NAVIRES_DISPONIBLES = [
        ("Porte-avions", 5),
        ("Croiseur", 4),
        ("Destroyer1", 3),
        ("Destroyer2", 3),
        ("Sous-marin1", 2),
        ("Sous-marin2", 2)
    ]

    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []           # positions sur le plateau (à renseigner plus tard)
        self.positions_touchees = []  # cases où le navire a été touché

    def est_coule(self):
        """
        Vérifie si le navire est coulé.
        Un navire est coulé lorsque toutes ses positions
        ont été touchées.
        """
        return len(self.positions_touchees) == self.taille


# --------------------------------
# Classe Joueur
# --------------------------------
class Joueur:
    """
    Représente un joueur (humain ou ordinateur).
    Contient la liste des navires et d'autres informations
    nécessaires au jeu.
    """
    def __init__(self, nom):
        self.nom = nom
        self.navires = []

    def initialiser_navires(self):
        """
        Initialise les navires du joueur à partir de la liste
        Navire.NAVIRES_DISPONIBLES. Le placement n'est pas encore géré
        dans cette phase.
        """
        for (nom, taille) in Navire.NAVIRES_DISPONIBLES:
            navire = Navire(nom, taille)
            self.navires.append(navire)


# --------------------------------
# Classe Plateau
# --------------------------------
class Plateau:
    """
    Gère le plateau de jeu (la grille).
    Dans cette phase, on prépare juste le cadrillage via un Canvas,
    sans afficher de fenêtre complète (phase 2).
    """
    def __init__(self, parent=None, rows=10, cols=10, cell_size=30):
        # Le paramètre parent est prévu pour la phase 2
        # (quand nous aurons une fenêtre Tk).
        # Ici, nous le rendons optionnel pour la phase 1.
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Préparation d'un Canvas (non utilisé en phase 1)
        self.canvas = tk.Canvas(
            self.parent,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white"
        )

        # Dessin du quadrillage
        self.draw_grid()

    def draw_grid(self):
        """
        Dessine les lignes de la grille (10 x 10 par défaut).
        Dans cette phase 1, nous ne l'affichons pas encore à l'écran.
        """
        for i in range(self.rows + 1):
            self.canvas.create_line(
                0,
                i * self.cell_size,
                self.cols * self.cell_size,
                i * self.cell_size,
                fill="black"
            )
        for j in range(self.cols + 1):
            self.canvas.create_line(
                j * self.cell_size,
                0,
                j * self.cell_size,
                self.rows * self.cell_size,
                fill="black"
            )



