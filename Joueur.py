import random
from Navire import *
class Joueur:
    """
    Classe Joueur
    ------------
    Représente un joueur (humain ou IA).

    Attributs principaux :
    - nom (str) : le nom du joueur
    - navires (list[Navire]) : la liste de tous ses navires
    - grille (list[list[Navire|None]]) : grille 10x10, None si vide
    - tirs_effectues (set[tuple[int, int]]) : ensemble des coups déjà tirés
    - mode_difficile (bool) : True si l'IA est en mode difficile (cases
      adjacentes ciblées après un tir touché), False sinon
    - reserve_cibles_proches (list[tuple[int, int]]) : liste des cases à
      cibler en priorité quand un navire vient d'être touché (IA difficile)
    - tirs_reussis (int) : nombre de tirs réussis (touché ou coulé)
    - tirs_rates (int) : nombre de tirs ratés (manqué)
    """
    def __init__(self, nom):
        self.nom = nom
        self.navires = []
        # Grille 10x10 : None => case vide, sinon référence vers un Navire
        self.grille = [[None for _ in range(10)] for _ in range(10)]
        # Liste des coups déjà tirés (row, col)
        self.tirs_effectues = set()

        # Pour la difficulté IA
        self.mode_difficile = False
        self.reserve_cibles_proches = []

        # Pour le comptage des tirs
        self.tirs_reussis = 0
        self.tirs_rates = 0

    def toggle_mode_difficile(self):
        """
        Bascule le mode difficile :
        - True => IA tire sur les cases adjacentes quand un tir est touché
        - False => IA tire de façon totalement aléatoire
        """
        self.mode_difficile = not self.mode_difficile
        mode_str = "DIFFICILE" if self.mode_difficile else "FACILE"
        print(f"[INFO] Le mode de {self.nom} est maintenant : {mode_str}")

    def initialiser_navires(self):
        """
        Crée tous les navires définis dans Navire.NAVIRES_DISPONIBLES
        et les ajoute à la liste self.navires.
        """
        for (nom, taille) in Navire.NAVIRES_DISPONIBLES:
            navire = Navire(nom, taille)
            self.navires.append(navire)

    def navires_non_places(self):
        """
        Retourne la liste des navires pas encore positionnés (i.e.
        ceux dont la liste positions est vide).
        """
        return [n for n in self.navires if not n.positions]

    def get_navire_by_name(self, name):
        """
        Retourne l'objet Navire portant le nom 'name',
        ou None si introuvable.
        """
        for n in self.navires:
            if n.nom == name:
                return n
        return None

    def peut_placer_navire(self, navire, start_row, start_col, orientation):
        """
        Vérifie si le navire (Navire) peut être placé à (start_row, start_col)
        en orientation 'H' (horizontal) ou 'V' (vertical),
        sans chevaucher un autre navire ou sortir de la grille.
        """
        if orientation == 'H':
            if start_col + navire.taille > 10:
                return False
            for c in range(start_col, start_col + navire.taille):
                if self.grille[start_row][c] is not None:
                    return False
        else:  # 'V'
            if start_row + navire.taille > 10:
                return False
            for r in range(start_row, start_row + navire.taille):
                if self.grille[r][start_col] is not None:
                    return False
        return True

    def placer_navire(self, navire, start_row, start_col, orientation):
        """
        Place le navire (Navire) dans la grille (self.grille)
        et assigne ses positions (navire.positions).
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
        Place tous les navires de façon aléatoire (pour l'ordinateur).
        Tente un placement jusqu'à ce que tous les navires soient positionnés.
        """
        for navire in self.navires:
            placed = False
            while not placed:
                ori = random.choice(["H", "V"])
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                if self.peut_placer_navire(navire, row, col, ori):
                    self.placer_navire(navire, row, col, ori)
                    placed = True

    def tirer_sur(self, autre_joueur, row, col):
        """
        Le joueur (self) tire sur la grille de 'autre_joueur' à (row, col).
        Retourne : "touche", "coule", "manque" ou "deja_tire".

        Met à jour self.tirs_reussis ou self.tirs_rates en fonction du résultat.
        """
        # Vérification si déjà tiré
        if (row, col) in self.tirs_effectues:
            return "deja_tire"
        self.tirs_effectues.add((row, col))

        navire = autre_joueur.grille[row][col]
        if navire is None:
            # Tir manqué
            self.tirs_rates += 1
            return "manque"
        else:
            # Tir touché
            if (row, col) not in navire.positions_touchees:
                navire.positions_touchees.append((row, col))

            # On incrémente les tirs réussis
            self.tirs_reussis += 1

            # Vérifier si le navire est coulé
            if navire.est_coule():
                return "coule"
            else:
                return "touche"

    def tous_navires_coules(self):
        """
        Retourne True si tous les navires du joueur
        (self.navires) sont coulés, False sinon.
        """

        return all(navire.est_coule() for navire in self.navires)

