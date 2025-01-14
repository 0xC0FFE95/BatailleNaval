from tkinter import *
from Joueur import *
class Plateau:
    """
    Gère l'affichage d'un plateau (10x10) dans un Canvas.
    - grid_color stocke la couleur "définitive" de chaque case.
    - preview_items stocke les ID graphiques pour un "preview" temporaire.
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
        et met à jour grid_color.
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
        sans modifier grid_color.
        """
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        return rect_id

    def redraw_all_cells(self):
        """Redessine toutes les cases permanentes (utile après reset)."""
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.grid_color[r][c]
                self.color_cell(r, c, color)

    def toggle_orientation(self):
        self.orientation_joueur.set("V" if self.orientation_joueur.get() == "H" else "H")
        print(f"[INFO] Orientation : {self.orientation_joueur.get()}")

