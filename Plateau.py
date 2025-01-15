from tkinter import *
from Joueur import *
class Plateau:
    """
    Classe Plateau
    -------------
    Gère l'affichage d'un plateau (10x10) dans un Canvas Tkinter,
    ainsi que les sons associés (tir, touche, coule).

    Attributs principaux :
    - parent (Tk ou Frame) : le parent Tkinter
    - rows, cols (int) : dimensions de la grille (par défaut 10x10)
    - cell_size (int) : taille d'une cellule en pixels
    - canvas (Canvas) : le canevas Tkinter où est dessinée la grille
    - grid_color (list[list[str]]) : couleur "définitive" de chaque case
    - preview_items (list[int]) : liste des ID graphiques (rectangles) temporaires
    - joueur (Joueur) : le Joueur associé à ce plateau
    - ordinateur (Joueur) : l'adversaire (IA)

    Méthodes principales :
    - draw_grid() : dessine la grille initiale
    - color_cell(row, col, color) : colorie de façon permanente une case
    - clear_preview() : efface la prévisualisation
    - color_preview_cell(row, col, color) : colorie une case en mode preview
    - redraw_all_cells() : redessine toutes les cases permanentes
    - toggle_orientation() : change l'orientation de placement (H/V)
    - play_sound_tir(), play_sound_touche(), play_sound_coule() :
      méthodes pour jouer les sons associés.
    """
    def __init__(self, parent, rows=10, cols=10, cell_size=30):
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        self.canvas = Canvas(
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white"
        )
        self.draw_grid()

        # Couleur réelle de chaque case
        self.grid_color = [["white" for _ in range(self.cols)] for _ in range(self.rows)]
        # Éléments temporaires (preview)
        self.preview_items = []

        # Création des Joueurs
        self.joueur = Joueur("Humain")
        self.joueur.initialiser_navires()

        self.ordinateur = Joueur("Ordinateur")
        self.ordinateur.initialiser_navires()
        self.ordinateur.placement_aleatoire()

        self.orientation_joueur = StringVar()
        self.orientation_joueur.set("H")

        # Phase de jeu : "placement" ou "battle"
        self.phase = StringVar()
        self.phase.set("placement")  # Par défaut, on est en phase de placement

    def draw_grid(self):
        """Dessine la grille (lignes noires) dans le canvas."""
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

    def color_cell(self, row, col, color):
        """
        Colorie la case (row, col) en 'color' de façon PERMANENTE,
        et met à jour self.grid_color.
        """
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        self.grid_color[row][col] = color

    def clear_preview(self):
        """Supprime les éléments graphiques de prévisualisation."""
        for item_id in self.preview_items:
            self.canvas.delete(item_id)
        self.preview_items.clear()

    def color_preview_cell(self, row, col, color):
        """
        Colorie la case (row, col) en 'color' TEMPORAIREMENT,
        sans modifier self.grid_color.
        Retourne l'ID de l'objet graphique créé, afin de pouvoir le supprimer.
        """
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        return rect_id

    def redraw_all_cells(self):
        """
        Redessine toutes les cases permanentes (utile après reset ou nouvelle partie).
        """
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.grid_color[r][c]
                self.color_cell(r, c, color)

    def toggle_orientation(self):
        """
        Bascule l'orientation de placement entre 'H' et 'V'.
        """
        self.orientation_joueur.set("V" if self.orientation_joueur.get() == "H" else "H")
        print(f"[INFO] Orientation : {self.orientation_joueur.get()}")

