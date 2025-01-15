from tkinter import *
import random
import time
from Joueur import *
from Plateau import *








def main():
    """
    Fonction main() : Point d'entrée de l'application Bataille Navale.
    Configure la fenêtre Tk, instancie les plateaux, gère l'interface,
    les événements de souris, le bouton "Valider", etc.
    """

    root = Tk()
    root.title("Bataille Navale")

    # ---------------------------------------------------------------------------------
    # 1) Création des joueurs (Humain, Ordinateur) et de leurs plateaux respectifs
    # ---------------------------------------------------------------------------------
    joueur = Joueur("Humain")
    joueur.initialiser_navires()

    ordinateur = Joueur("Ordinateur")
    ordinateur.initialiser_navires()
    ordinateur.placement_aleatoire()

    # Pour gérer l'orientation (H ou V) lors du placement
    orientation_joueur = StringVar()
    orientation_joueur.set("H")

    # Phase de jeu : "placement" ou "battle" ou "fin"
    phase = StringVar()
    phase.set("placement")  # Par défaut, phase de placement

    # On stocke le temps de début lorsqu'on clique sur "Valider"
    start_time = None
    game_in_progress = False

    # ---------------------------------------------------------------------------------
    # 2) Création de l'interface : 2 Canevas pour l'affichage des grilles
    # ---------------------------------------------------------------------------------
    # -- Plateau Ordinateur --
    frame_ordi = Frame(root)
    frame_ordi.pack(side=LEFT, padx=10, pady=10)

    label_ordi = Label(frame_ordi, text="Ordinateur", font=("Arial", 14, "bold"))
    label_ordi.pack()

    canvas_ordinateur = Canvas(frame_ordi, width=350, height=400, bg="lightgreen")
    canvas_ordinateur.pack()

    plateau_ordinateur = Plateau(canvas_ordinateur)
    # On va simplement réutiliser le plateau_ordinateur.canvas
    canvas_ordinateur.create_window(
        30, 50,
        window=plateau_ordinateur.canvas,
        anchor="nw"
    )

    # -- Plateau Joueur --
    frame_joueur = Frame(root)
    frame_joueur.pack(side=LEFT, padx=10, pady=10)

    label_joueur = Label(frame_joueur, text="Joueur", font=("Arial", 14, "bold"))
    label_joueur.pack()

    canvas_joueur = Canvas(frame_joueur, width=350, height=400, bg="lightblue")
    canvas_joueur.pack()

    plateau_joueur = Plateau(canvas_joueur)
    canvas_joueur.create_window(
        30, 50,
        window=plateau_joueur.canvas,
        anchor="nw"
    )

    # ---------------------------------------------------------------------------------
    # 3) Zone de boutons / sélection navire / difficultés / stats
    # ---------------------------------------------------------------------------------
    frame_boutons = Frame(root, bg="lightgray")
    frame_boutons.pack(side=LEFT, fill=Y, padx=10, pady=10)

    # --- Liste déroulante des navires à placer ---
    def liste_noms_non_places():
        return [n.nom for n in joueur.navires_non_places()]

    selected_navire_name = StringVar()
    noms_init = liste_noms_non_places()
    if noms_init:
        selected_navire_name.set(noms_init[0])
    else:
        selected_navire_name.set("Aucun")

    om_navires = OptionMenu(frame_boutons, selected_navire_name, *noms_init)
    om_navires.config(width=15)
    om_navires.pack(pady=5)

    # --- Bouton Orientation ---
    def toggle_orientation():
        orientation_joueur.set("V" if orientation_joueur.get() == "H" else "H")
        print(f"[INFO] Orientation : {orientation_joueur.get()}")

    btn_orientation = Button(frame_boutons, text="Orientation H/V", command=toggle_orientation)
    btn_orientation.pack(pady=5)

    # --- Bouton Mode Difficile (pour l'ordinateur) ---
    def toggle_difficulty():
        ordinateur.toggle_mode_difficile()
        # On peut mettre à jour le texte du bouton si on veut
        new_text = "Mode Facile" if not ordinateur.mode_difficile else "Mode Difficile"
        btn_difficulty.config(text=new_text)

    btn_difficulty = Button(frame_boutons, text="Mode Difficile", command=toggle_difficulty)
    btn_difficulty.pack(pady=5)

    # --- Bouton Valider (fin de phase placement => phase battle) ---
    def valider():
        """
        Passe en phase 'battle' si tous les navires sont placés,
        enregistre l'heure de début, et lance l'actualisation du temps.
        """
        nonlocal start_time, game_in_progress
        if not joueur.navires_non_places():
            phase.set("battle")
            start_time = time.time()
            game_in_progress = True
            update_game_time()
            print("[INFO] Début de la bataille !")
        else:
            print("[INFO] Il reste des navires à placer !")

    btn_valider = Button(frame_boutons, text="Valider", command=valider)
    btn_valider.pack(pady=5)

    # --- Label pour l'affichage du temps ---
    label_time = Label(frame_boutons, text="Temps : 0 s", font=("Arial", 12, "bold"))
    label_time.pack(pady=5)

    def update_game_time():
        """
        Met à jour le label du temps de jeu toutes les secondes
        tant que 'game_in_progress' est True.
        """
        if game_in_progress and start_time is not None:
            elapsed = int(time.time() - start_time)
            label_time.config(text=f"Temps : {elapsed} s")
            root.after(1000, update_game_time)

    # --- Labels pour les stats de tirs ---
    label_joueur_stats = Label(frame_boutons, text="Joueur: 0 réussis / 0 ratés")
    label_joueur_stats.pack(pady=5)

    label_ordi_stats = Label(frame_boutons, text="Ordinateur: 0 réussis / 0 ratés")
    label_ordi_stats.pack(pady=5)

    def maj_labels_stats():
        """
        Met à jour les labels de statistiques pour le joueur et l'ordinateur.
        """
        label_joueur_stats.config(
            text=f"{joueur.nom}: {joueur.tirs_reussis} réussis / {joueur.tirs_rates} ratés"
        )
        label_ordi_stats.config(
            text=f"{ordinateur.nom}: {ordinateur.tirs_reussis} réussis / {ordinateur.tirs_rates} ratés"
        )

    # --- Bouton Nouvelle Partie ---
    def nouvelle_partie():
        print("[INFO] Nouvelle partie !")
        root.destroy()
        main()

    btn_nouvelle_partie = Button(frame_boutons, text="Nouvelle Partie", command=nouvelle_partie)
    btn_nouvelle_partie.pack(pady=5)

    # --- Bouton Quitter ---
    def quitter_jeu():
        root.quit()

    btn_quitter = Button(frame_boutons, text="Quitter", command=quitter_jeu)
    btn_quitter.pack(pady=5)

    # ---------------------------------------------------------------------------------
    # 4) Gestion des événements de placement (plateau du joueur)
    # ---------------------------------------------------------------------------------
    preview_is_valid = False

    def motion_joueur(event):
        """Prévisualisation du placement (uniquement en phase 'placement')."""
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

        nonlocal preview_is_valid
        preview_is_valid = valid

    def click_joueur(event):
        """
        Clic sur le plateau du joueur : on place un navire (si possible)
        uniquement en phase de placement.
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

            restants = liste_noms_non_places()
            om_navires["menu"].delete(0, "end")

            if restants:
                # Re-remplir l'OptionMenu
                for nm in restants:
                    om_navires["menu"].add_command(label=nm, command=lambda v=nm: selected_navire_name.set(v))
                selected_navire_name.set(restants[0])
            else:
                selected_navire_name.set("Aucun")
                print("[INFO] Tous les navires sont placés !")

            plateau_joueur.clear_preview()
            preview_is_valid = False
        else:
            print("[INFO] Placement invalide.")

    plateau_joueur.canvas.bind("<Motion>", motion_joueur)
    plateau_joueur.canvas.bind("<Button-1>", click_joueur)

    # ---------------------------------------------------------------------------------
    # 5) Logique de bataille : Clic sur le plateau de l'Ordinateur
    # ---------------------------------------------------------------------------------
    def on_click_ordinateur(event):
        """
        Quand on clique sur la grille de l'Ordinateur en phase battle,
        le joueur tire sur l'ordinateur, puis l'ordinateur riposte.
        On joue également les sons (tir, touche, coule).
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
            print(f"[JOUEUR] Tir à ({row}, {col}): MANQUÉ")
            plateau_ordinateur.color_cell(row, col, "blue")

        elif result == "touche":
            print(f"[JOUEUR] Tir à ({row}, {col}): TOUCHÉ")
            plateau_ordinateur.color_cell(row, col, "red")
        elif result == "coule":
            print(f"[JOUEUR] Tir à ({row}, {col}): NAVIRE COULÉ !")
            nav_coule = ordinateur.grille[row][col]
            for (r, c) in nav_coule.positions:
                plateau_ordinateur.color_cell(r, c, "black")

        # Mettre à jour les stats
        maj_labels_stats()
        # Vérifier si l'ordinateur a perdu
        if ordinateur.tous_navires_coules():
            print("=== VICTOIRE DU JOUEUR !!! ===")
            phase.set("fin")
            return

        # 2) Tour de l'ordinateur (IA)
        ai_shot = None
        if ordinateur.mode_difficile and ordinateur.reserve_cibles_proches:
            # Si on a des cibles en réserve (cases adjacentes d'un dernier tir touché)
            ai_shot = ordinateur.reserve_cibles_proches.pop(0)
            while ai_shot in ordinateur.tirs_effectues:
                # On prend la suivante si déjà tirée
                if not ordinateur.reserve_cibles_proches:
                    ai_shot = None
                    break
                ai_shot = ordinateur.reserve_cibles_proches.pop(0)

        if ai_shot is None:
            # Tir aléatoire
            possible_cells = [(r, c) for r in range(10) for c in range(10)
                              if (r, c) not in ordinateur.tirs_effectues]
            if not possible_cells:
                print("=== L'ordinateur ne peut plus tirer. Match nul ? ===")
                phase.set("fin")
                return
            ai_shot = random.choice(possible_cells)

        (ai_row, ai_col) = ai_shot
        ai_result = ordinateur.tirer_sur(joueur, ai_row, ai_col)

        if ai_result == "manque":
            plateau_joueur.color_cell(ai_row, ai_col, "blue")
            print(f"[ORDI] Tir à ({ai_row}, {ai_col}): MANQUÉ")
        elif ai_result == "touche":
            print(f"[ORDI] Tir à ({ai_row}, {ai_col}): TOUCHÉ")
            plateau_joueur.color_cell(ai_row, ai_col, "red")
            # En mode difficile, l'IA ajoute les cases adjacentes dans reserve_cibles_proches
            if ordinateur.mode_difficile:
                directions = [(-1,0), (1,0), (0,-1), (0,1)]
                for (dr, dc) in directions:
                    nr, nc = ai_row + dr, ai_col + dc
                    if 0 <= nr < 10 and 0 <= nc < 10:
                        if (nr, nc) not in ordinateur.tirs_effectues:
                            ordinateur.reserve_cibles_proches.append((nr, nc))

        elif ai_result == "coule":
            print(f"[ORDI] Tir à ({ai_row}, {ai_col}): NAVIRE COULÉ !")
            nav_coule = joueur.grille[ai_row][ai_col]
            for (r, c) in nav_coule.positions:
                plateau_joueur.color_cell(r, c, "black")

        # Mettre à jour les stats
        maj_labels_stats()

        # Vérifier si le joueur a tout perdu
        if joueur.tous_navires_coules():
            print("=== L'ORDINATEUR GAGNE !!! ===")
            phase.set("fin")


    plateau_ordinateur.canvas.bind("<Button-1>", on_click_ordinateur)

    root.mainloop()


if __name__ == "__main__":
    main()
