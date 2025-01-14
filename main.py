
from Plateau import *
from Joueur import *
from Navire import *

# --------------------------------
# PHASE 4 : Placement + VALIDATION + Bataille
# --------------------------------


def main():
    root = Tk()
    root.title("Bataille Navale")

    # -------------------------------------------------------
    # 1) Logique des joueurs
    # -------------------------------------------------------
    joueur = Joueur("Humain")
    joueur.initialiser_navires()

    ordinateur = Joueur("Ordinateur")
    ordinateur.initialiser_navires()
    ordinateur.placement_aleatoire()

    orientation_joueur = StringVar()
    orientation_joueur.set("H")

    # Phase de jeu : "placement" ou "battle"
    phase = StringVar()
    phase.set("placement")  # Par défaut, on est en phase de placement

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
        30, 50,
        window=plateau_ordinateur.canvas,
        anchor="nw"
    )
    # -------------------------------------------------------
    # 2) Interface : Plateau Joueur
    # -------------------------------------------------------
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

    # -------------------------------------------------------
    # 3) Interface : Plateau Ordinateur
    # -------------------------------------------------------


    # -------------------------------------------------------
    # 4) Interface : Zone de Boutons / Sélection Navire
    # -------------------------------------------------------
    canvas_boutons = Canvas(root, width=200, height=400, bg="lightgray")
    canvas_boutons.pack(side=LEFT, padx=10, pady=10)

    # A) Sélection du navire à placer
    def liste_noms_non_places():
        return [n.nom for n in joueur.navires_non_places()]

    selected_navire_name = StringVar()
    noms_init = liste_noms_non_places()
    if noms_init:
        selected_navire_name.set(noms_init[0])
    else:
        selected_navire_name.set("Aucun")

    om_navires = OptionMenu(canvas_boutons, selected_navire_name, *noms_init)
    canvas_boutons.create_window(100, 30, window=om_navires, anchor="center")

    # B) Bouton Orientation
    def toggle_orientation():
        orientation_joueur.set("V" if orientation_joueur.get() == "H" else "H")
        print(f"[INFO] Orientation : {orientation_joueur.get()}")

    btn_orientation = Button(canvas_boutons, text="Orientation H/V", command=toggle_orientation)
    canvas_boutons.create_window(100, 70, window=btn_orientation, anchor="center")

    # C) Bouton Valider (apparaît quand tous les navires sont placés)
    btn_valider = Button(canvas_boutons, text="Valider", state=DISABLED, command=lambda: phase.set("battle"))
    canvas_boutons.create_window(100, 110, window=btn_valider, anchor="center")

    # D) Bouton Nouvelle Partie
    def nouvelle_partie():
        print("[INFO] Nouvelle partie !")
        root.destroy()
        main()

    btn_nouvelle_partie = Button(canvas_boutons, text="Nouvelle Partie", command=nouvelle_partie)
    canvas_boutons.create_window(100, 150, window=btn_nouvelle_partie, anchor="center")

    # E) Bouton Quitter
    def quitter_jeu():
        root.quit()

    btn_quitter = Button(canvas_boutons, text="Quitter", command=quitter_jeu)
    canvas_boutons.create_window(100, 190, window=btn_quitter, anchor="center")

    # -------------------------------------------------------
    # 5) Prévisualisation + Placement
    # -------------------------------------------------------
    preview_is_valid = False

    def motion_joueur(event):
        """Prévisualisation (uniquement si on est en 'placement')."""
        if phase.get() != "placement":
            return

        plateau_joueur.clear_preview()

        nav_name = selected_navire_name.get()
        if nav_name == "Aucun":
            return
        navire = joueur.get_navire_by_name(nav_name)
        if not navire:
            return

        row = event.y // plateau_joueur.cell_size
        col = event.x // plateau_joueur.cell_size
        if not (0 <= row < 10 and 0 <= col < 10):
            return

        ori = orientation_joueur.get()
        valid = joueur.peut_placer_navire(navire, row, col, ori)
        color_preview = "green" if valid else "red"

        coords = []
        if ori == 'H':
            if col + navire.taille <= 10:
                coords = [(row, c) for c in range(col, col + navire.taille)]
        else:
            if row + navire.taille <= 10:
                coords = [(r, col) for r in range(row, row + navire.taille)]

        for (r, c) in coords:
            rect_id = plateau_joueur.color_preview_cell(r, c, color_preview)
            plateau_joueur.preview_items.append(rect_id)

        # Mettre à jour la variable preview_is_valid dans la closure
        nonlocal preview_is_valid
        preview_is_valid = valid

    def click_joueur(event):
        """
        Clic gauche sur le plateau du joueur : on place si en phase de placement,
        sinon, on ne fait rien.
        """
        if phase.get() != "placement":
            return

        nonlocal preview_is_valid
        nav_name = selected_navire_name.get()
        if nav_name == "Aucun":
            print("[INFO] Aucun navire à placer.")
            return
        navire = joueur.get_navire_by_name(nav_name)
        if not navire:
            return

        row = event.y // plateau_joueur.cell_size
        col = event.x // plateau_joueur.cell_size

        if preview_is_valid and joueur.peut_placer_navire(navire, row, col, orientation_joueur.get()):
            # Placement effectif
            joueur.placer_navire(navire, row, col, orientation_joueur.get())
            for (r, c) in navire.positions:
                plateau_joueur.color_cell(r, c, "gray")

            # Mise à jour OptionMenu
            restants = liste_noms_non_places()
            if restants:
                selected_navire_name.set(restants[0])
                om_navires["menu"].delete(0, "end")
                for nm in restants:
                    om_navires["menu"].add_command(label=nm, command=lambda v=nm: selected_navire_name.set(v))
            else:
                selected_navire_name.set("Aucun")
                om_navires["menu"].delete(0, "end")
                print("[INFO] Tous les navires sont placés !")
                # Activer le bouton "Valider"
                btn_valider.config(state=NORMAL)

            plateau_joueur.clear_preview()
            preview_is_valid = False
        else:
            print("[INFO] Placement invalide.")

    plateau_joueur.canvas.bind("<Motion>", motion_joueur)
    plateau_joueur.canvas.bind("<Button-1>", click_joueur)

    # -------------------------------------------------------
    # 6) Logique de bataille
    # -------------------------------------------------------
    def on_click_ordinateur(event):
        """
        Quand on clique sur la grille de l'Ordinateur (phase bataille), on tire.
        """
        if phase.get() != "battle":
            return  # On ne tire que si la phase est "battle"

        row = event.y // plateau_ordinateur.cell_size
        col = event.x // plateau_ordinateur.cell_size

        if not (0 <= row < 10 and 0 <= col < 10):
            return

        # 1) Le joueur (Humain) tire sur l'ordi
        result = joueur.tirer_sur(ordinateur, row, col)
        if result == "deja_tire":
            print("[INFO] Vous avez déjà tiré ici !")
            return
        elif result == "manque":
            print("[JOUEUR] Tir à ({}, {}): MANQUÉ".format(row, col))
            plateau_ordinateur.color_cell(row, col, "blue")  # Eau manquée
        elif result == "touche":
            print("[JOUEUR] Tir à ({}, {}): TOUCHÉ".format(row, col))
            plateau_ordinateur.color_cell(row, col, "red")
        elif result == "coule":
            print("[JOUEUR] Tir à ({}, {}): NAVIRE COULÉ !".format(row, col))
            # Colorier tout le navire en noir
            nav_coule = ordinateur.grille[row][col]  # c'est le navire coulé
            for (r, c) in nav_coule.positions:
                plateau_ordinateur.color_cell(r, c, "black")

        # Vérifier si l'ordinateur a tout perdu
        if ordinateur.tous_navires_coules():
            print("=== VICTOIRE DU JOUEUR !!! ===")
            phase.set("fin")
            return

        # 2) L'ordinateur riposte
        # On cherche un tir aléatoire *non déjà tiré* sur la grille du joueur
        possible_cells = [(r, c) for r in range(10) for c in range(10)
                          if (r, c) not in ordinateur.tirs_effectues]
        if not possible_cells:
            # Plus de coups disponibles ?
            print("=== L'ordinateur ne peut plus tirer. Match nul ? ===")
            phase.set("fin")
            return

        (ai_row, ai_col) = random.choice(possible_cells)
        ai_result = ordinateur.tirer_sur(joueur, ai_row, ai_col)

        if ai_result == "manque":
            print("[ORDI] Tir à ({}, {}): MANQUÉ".format(ai_row, ai_col))
            plateau_joueur.color_cell(ai_row, ai_col, "blue")
        elif ai_result == "touche":
            print("[ORDI] Tir à ({}, {}): TOUCHÉ".format(ai_row, ai_col))
            plateau_joueur.color_cell(ai_row, ai_col, "red")
        elif ai_result == "coule":
            print("[ORDI] Tir à ({}, {}): NAVIRE COULÉ !".format(ai_row, ai_col))
            nav_coule = joueur.grille[ai_row][ai_col]
            for (r, c) in nav_coule.positions:
                plateau_joueur.color_cell(r, c, "black")

        # Vérifier si le joueur a tout perdu
        if joueur.tous_navires_coules():
            print("=== L'ORDINATEUR GAGNE !!! ===")
            phase.set("fin")

    plateau_ordinateur.canvas.bind("<Button-1>", on_click_ordinateur)

    root.mainloop()


if __name__ == "__main__":
    main()
