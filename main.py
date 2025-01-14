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


class Plateau:
    """
    Gère le plateau de jeu (la grille).
    Dans la phase 2, on utilise un Canvas pour afficher la grille
    dans une interface Tkinter.
    """
    def __init__(self, parent, rows=10, cols=10, cell_size=30):
        """
        :param parent: le widget parent (un Canvas dans notre cas).
        :param rows: nombre de lignes du plateau.
        :param cols: nombre de colonnes du plateau.
        :param cell_size: taille d'une cellule (en pixels).
        """
        self.parent = parent   # ATTENTION : ce parent est un Canvas (et non une fenêtre)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Création d'un Canvas (pour le quadrillage) qui sera placé DANS le parent-canvas
        self.canvas = Canvas(
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white"
        )
        # draw_grid uniquement après la création
        self.draw_grid()

    def draw_grid(self):
        """
        Dessine les lignes de la grille (10 x 10 par défaut).
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


def main():
    root = Tk()
    root.title("Bataille Navale - Phase 2 (Canvas)")

    # Fonctions liées aux boutons
    def nouvelle_partie():
        print("[INFO] Nouvelle partie !")
        # Ici, vous pourriez réinitialiser les plateaux, re-créer les navires, etc.

    def quitter_jeu():
        root.quit()

    # --- Premier Canvas : pour le plateau Joueur ---
    canvas_joueur = Canvas(root, width=350, height=400, bg="lightblue")
    canvas_joueur.pack(side=LEFT, padx=10, pady=10)

    # Ajout d'un texte (label) "Joueur" dans ce Canvas
    canvas_joueur.create_text(
        100, 20,   # Position X=100, Y=20
        text="Joueur",
        font=("Arial", 14, "bold"),
        fill="black"
    )

    # Création du plateau Joueur (grille)
    plateau_joueur = Plateau(canvas_joueur)
    # On place le Canvas de la grille DANS le Canvas "canvas_joueur" via create_window
    canvas_joueur.create_window(
        30, 50,        # Coordonnées (x, y) dans le canvas_joueur
        window=plateau_joueur.canvas,
        anchor="nw"    # ancrage en haut à gauche
    )

    # --- Événement de clic sur le plateau du joueur ---
    def on_click_joueur(event):
        # Calculer la ligne et la colonne en fonction de la position du clic
        row = event.y // plateau_joueur.cell_size
        col = event.x // plateau_joueur.cell_size
        print(f"[Joueur] Clic sur la cellule ({row}, {col})")

    # On associe la fonction au clic gauche de la souris sur le Canvas de la grille
    plateau_joueur.canvas.bind("<Button-1>", on_click_joueur)

    # --- Deuxième Canvas : pour le plateau Ordinateur ---
    canvas_ordinateur = Canvas(root, width=350, height=400, bg="lightgreen")
    canvas_ordinateur.pack(side=LEFT, padx=10, pady=10)

    # Ajout d'un texte (label) "Ordinateur" dans ce Canvas
    canvas_ordinateur.create_text(
        120, 20,
        text="Ordinateur",
        font=("Arial", 14, "bold"),
        fill="black"
    )

    # Création du plateau Ordinateur (grille)
    plateau_ordinateur = Plateau(canvas_ordinateur)
    # Placement dans le canvas_ordinateur
    canvas_ordinateur.create_window(
        50, 50,
        window=plateau_ordinateur.canvas,
        anchor="nw"
    )

    # --- Troisième Canvas : pour les boutons globaux ---
    canvas_boutons = Canvas(root, width=150, height=400, bg="lightgray")
    canvas_boutons.pack(side=LEFT, padx=10, pady=10)

    # On crée des boutons et on les place via create_window
    btn_nouvelle_partie = Button(canvas_boutons, text="Nouvelle Partie", command=nouvelle_partie)
    canvas_boutons.create_window(
        75, 50,  # au centre (X=75) si la largeur du canvas_boutons est ~150
        window=btn_nouvelle_partie,
        anchor="center"
    )

    btn_quitter = Button(canvas_boutons, text="Quitter", command=quitter_jeu)
    canvas_boutons.create_window(
        75, 100,
        window=btn_quitter,
        anchor="center"
    )

    # --- Création des joueurs ---
    joueur = Joueur("Humain")
    joueur.initialiser_navires()

    ordinateur = Joueur("Ordinateur")
    ordinateur.initialiser_navires()

    # Lancement de la boucle événementielle Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
