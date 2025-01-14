from tkinter import *
import random

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
        self.positions = []           # positions (liste de (row, col)) sur le plateau
        self.positions_touchees = []  # cases où le navire a été touché

    def est_coule(self):
        """Vérifie si le navire est coulé."""
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
        # Grille 10x10 : None => case vide, sinon référence vers un Navire
        self.grille = [[None for _ in range(10)] for _ in range(10)]

    def initialiser_navires(self):
        for (nom, taille) in Navire.NAVIRES_DISPONIBLES:
            navire = Navire(nom, taille)
            self.navires.append(navire)

    def navires_non_places(self):
        """
        Retourne la liste des navires qui n'ont pas encore de positions.
        """
        return [n for n in self.navires if len(n.positions) == 0]

    def get_navire_by_name(self, name):
        """
        Récupère un objet Navire à partir de son nom (unique).
        """
        for n in self.navires:
            if n.nom == name:
                return n
        return None

    def peut_placer_navire(self, navire, start_row, start_col, orientation):
        """
        Vérifie si on peut placer 'navire' à partir de (start_row, start_col)
        en orientation 'H' ou 'V'.
        """
        if orientation == 'H':
            if start_col + navire.taille > 10:
                return False
            for c in range(start_col, start_col + navire.taille):
                if self.grille[start_row][c] is not None:
                    return False
        else:  # orientation == 'V'
            if start_row + navire.taille > 10:
                return False
            for r in range(start_row, start_row + navire.taille):
                if self.grille[r][start_col] is not None:
                    return False
        return True

    def placer_navire(self, navire, start_row, start_col, orientation):
        """
        Place effectivement le navire dans la grille,
        et remplit navire.positions.
        """
        navire.positions.clear()

        if orientation == 'H':
            for c in range(start_col, start_col + navire.taille):
                self.grille[start_row][c] = navire
                navire.positions.append((start_row, c))
        else:
            for r in range(start_row, start_row + navire.taille):
                self.grille[r][start_col] = navire
                navire.positions.append((r, start_col))

    def placement_aleatoire(self):
        """
        Place tous les navires de manière aléatoire (pour l'ordinateur).
        """
        for navire in self.navires:
            place = False
            while not place:
                orientation = random.choice(['H', 'V'])
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                if self.peut_placer_navire(navire, row, col, orientation):
                    self.placer_navire(navire, row, col, orientation)
                    place = True


# --------------------------------
# Classe Plateau
# --------------------------------
class Plateau:
    """
    Gère l'affichage d'un plateau (10x10) dans un Canvas.
    """
    def __init__(self, parent, rows=10, cols=10, cell_size=30):
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Canvas pour le quadrillage
        self.canvas = Canvas(
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white"
        )
        self.draw_grid()

        # Couleur finale de chaque case (stockée après placement confirmé)
        self.grid_color = [["white" for _ in range(self.cols)] for _ in range(self.rows)]

        # Liste des rectangles "preview" à effacer
        self.preview_items = []

    def draw_grid(self):
        """Dessine le quadrillage 10 x 10."""
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
        et met à jour la grille 'grid_color'.
        """
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # On stocke la couleur finale
        self.grid_color[row][col] = color

    def clear_preview(self):
        """
        Efface tous les rectangles de PREVIEW (temporaire).
        """
        for item_id in self.preview_items:
            self.canvas.delete(item_id)
        self.preview_items.clear()

    def color_preview_cell(self, row, col, color):
        """
        Colorie la case (row, col) en 'color' SANS modifier la couleur stockée.
        Retourne l'ID du rectangle créé pour l'effacer plus tard.
        """
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        return rect_id

    def redraw_all_cells(self):
        """
        Redessine toutes les cases permanentes (gris, blanc, etc.)
        (Au cas où on veuille rafraîchir la grille après un reset.)
        """
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.grid_color[r][c]
                self.color_cell(r, c, color)



# --------------------------------
# Phase 3 : Choix du navire + Prévisualisation (corrigée)
# --------------------------------
def main():
    root = Tk()
    root.title("Bataille Navale - Placement + Preview corrigé")

    orientation_joueur = StringVar()
    orientation_joueur.set("H")  # orientation par défaut : horizontale

    # Création des joueurs
    joueur = Joueur("Humain")
    joueur.initialiser_navires()
    ordinateur = Joueur("Ordinateur")
    ordinateur.initialiser_navires()
    ordinateur.placement_aleatoire()

    # --- Canvas de gauche : Plateau Joueur ---
    canvas_joueur = Canvas(root, width=350, height=400, bg="lightblue")
    canvas_joueur.pack(side=LEFT, padx=10, pady=10)

    canvas_joueur.create_text(
        100, 20,
        text="Joueur",
        font=("Arial", 14, "bold"),
        fill="black"
    )

    plateau_joueur = Plateau(canvas_joueur)
    canvas_joueur.create_window(
        30, 50,
        window=plateau_joueur.canvas,
        anchor="nw"
    )

    # --- Canvas de droite : Plateau Ordinateur ---
    canvas_ordinateur = Canvas(root, width=350, height=400, bg="lightgreen")
    canvas_ordinateur.pack(side=LEFT, padx=10, pady=10)

    canvas_ordinateur.create_text(
        120, 20,
        text="Ordinateur",
        font=("Arial", 14, "bold"),
        fill="black"
    )

    plateau_ordinateur = Plateau(canvas_ordinateur)
    canvas_ordinateur.create_window(
        50, 50,
        window=plateau_ordinateur.canvas,
        anchor="nw"
    )

    # --- Canvas pour les boutons / menu ---
    canvas_boutons = Canvas(root, width=180, height=400, bg="lightgray")
    canvas_boutons.pack(side=LEFT, padx=10, pady=10)

    # OptionMenu pour choisir quel navire placer
    def liste_noms_non_places():
        return [n.nom for n in joueur.navires_non_places()]

    selected_navire_name = StringVar()
    noms_init = liste_noms_non_places()
    if noms_init:
        selected_navire_name.set(noms_init[0])
    else:
        selected_navire_name.set("Aucun")

    om_navires = OptionMenu(canvas_boutons, selected_navire_name, *noms_init)
    canvas_boutons.create_window(
        90, 30,
        window=om_navires,
        anchor="center"
    )

    # Bouton pour changer orientation
    def toggle_orientation():
        if orientation_joueur.get() == "H":
            orientation_joueur.set("V")
        else:
            orientation_joueur.set("H")
        print(f"[INFO] Orientation sélectionnée : {orientation_joueur.get()}")

    btn_orientation = Button(canvas_boutons, text="Orientation H/V", command=toggle_orientation)
    canvas_boutons.create_window(
        90, 70,
        window=btn_orientation,
        anchor="center"
    )

    # Bouton Nouvelle Partie
    def nouvelle_partie():
        print("[INFO] Nouvelle partie !")
        root.destroy()
        main()

    btn_nouvelle_partie = Button(canvas_boutons, text="Nouvelle Partie", command=nouvelle_partie)
    canvas_boutons.create_window(
        90, 110,
        window=btn_nouvelle_partie,
        anchor="center"
    )

    # Bouton Quitter
    def quitter_jeu():
        root.quit()

    btn_quitter = Button(canvas_boutons, text="Quitter", command=quitter_jeu)
    canvas_boutons.create_window(
        90, 150,
        window=btn_quitter,
        anchor="center"
    )

    # ---------- PREVIEW ET PLACEMENT ----------
    preview_is_valid = False

    def motion_joueur(event):
        """
        À chaque déplacement de la souris, on prévisualise en rouge ou vert,
        sans modifier la couleur définitive.
        """
        nonlocal preview_is_valid

        # Effacer la prévisualisation précédente
        plateau_joueur.clear_preview()

        nav_name = selected_navire_name.get()
        if nav_name == "Aucun" or not nav_name:
            return  # Pas de navire à prévisualiser

        navire = joueur.get_navire_by_name(nav_name)
        if not navire:
            return

        row = event.y // plateau_joueur.cell_size
        col = event.x // plateau_joueur.cell_size
        # Hors grille ?
        if not (0 <= row < 10 and 0 <= col < 10):
            return

        ori = orientation_joueur.get()
        # Vérif si placement ok
        if joueur.peut_placer_navire(navire, row, col, ori):
            preview_color = "green"
            preview_is_valid = True
        else:
            preview_color = "red"
            preview_is_valid = False

        # Calcul des cases concernées
        coords = []
        if ori == 'H':
            if col + navire.taille <= 10:
                coords = [(row, c) for c in range(col, col + navire.taille)]
        else:
            if row + navire.taille <= 10:
                coords = [(r, col) for r in range(row, row + navire.taille)]

        for (r, c) in coords:
            rect_id = plateau_joueur.color_preview_cell(r, c, preview_color)
            plateau_joueur.preview_items.append(rect_id)

    def click_joueur(event):
        """
        Au clic, on place définitivement le navire si la preview est valide.
        """
        nonlocal preview_is_valid
        nav_name = selected_navire_name.get()
        if nav_name == "Aucun" or not nav_name:
            print("[INFO] Aucun navire sélectionné.")
            return
        navire = joueur.get_navire_by_name(nav_name)
        if not navire:
            return

        row = event.y // plateau_joueur.cell_size
        col = event.x // plateau_joueur.cell_size

        # Vérification
        if preview_is_valid and joueur.peut_placer_navire(navire, row, col, orientation_joueur.get()):
            # Placement effectif
            joueur.placer_navire(navire, row, col, orientation_joueur.get())

            # Colorier définitivement en gris
            for (r, c) in navire.positions:
                plateau_joueur.color_cell(r, c, "gray")

            print(f"[OK] Navire {navire.nom} placé sur la grille.")

            # Mettre à jour l'OptionMenu
            noms_restants = liste_noms_non_places()
            if noms_restants:
                selected_navire_name.set(noms_restants[0])
                # Mettre à jour le menu interne
                om_navires["menu"].delete(0, "end")
                for nm in noms_restants:
                    om_navires["menu"].add_command(label=nm, command=lambda v=nm: selected_navire_name.set(v))
            else:
                # Plus de navires à placer
                selected_navire_name.set("Aucun")
                om_navires["menu"].delete(0, "end")
                print("[INFO] Tous les navires du joueur sont placés !")

            # On efface la preview
            plateau_joueur.clear_preview()
            preview_is_valid = False
        else:
            print("[INFO] Placement invalide ou preview incorrect.")
    
    # Bind des événements
    plateau_joueur.canvas.bind("<Motion>", motion_joueur)
    plateau_joueur.canvas.bind("<Button-1>", click_joueur)

    root.mainloop()


if __name__ == "__main__":
    main()
