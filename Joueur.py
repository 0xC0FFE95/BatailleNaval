from Navire import *
import random
class Joueur:
    """
    Représente un joueur (humain ou IA).
    Contient la liste des navires et une grille 10x10 pour le placement.
    """
    def __init__(self, nom):
        self.nom = nom
        self.navires = []
        # Grille 10x10 : None => case vide, sinon référence vers un Navire
        self.grille = [[None for _ in range(10)] for _ in range(10)]
        # Liste des coups déjà tirés (row, col)
        self.tirs_effectues = set()

    def initialiser_navires(self):
        """Crée les navires définis dans Navire.NAVIRES_DISPONIBLES."""
        for (nom, taille) in Navire.NAVIRES_DISPONIBLES:
            navire = Navire(nom, taille)
            self.navires.append(navire)

    def navires_non_places(self):
        """Retourne la liste des navires pas encore positionnés."""
        return [n for n in self.navires if not n.positions]

    def get_navire_by_name(self, name):
        for n in self.navires:
            if n.nom == name:
                return n
        return None

    def peut_placer_navire(self, navire, start_row, start_col, orientation):
        """
        Vérifie si le navire peut être placé à (start_row, start_col)
        en orientation 'H' (horizontal) ou 'V' (vertical).
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
        """Place le navire dans la grille et assigne ses positions."""
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
        """Place tous les navires de façon aléatoire (pour l'ordinateur)."""
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
        Retourne : "touche", "coule", ou "manque".
        """
        # Vérification si déjà tiré
        if (row, col) in self.tirs_effectues:
            return "deja_tire"
        self.tirs_effectues.add((row, col))

        navire = autre_joueur.grille[row][col]
        if navire is None:
            return "manque"
        else:
            # Touché
            if (row, col) not in navire.positions_touchees:
                navire.positions_touchees.append((row, col))
            if navire.est_coule():
                return "coule"
            else:
                return "touche"

    def tous_navires_coules(self):
        """Retourne True si tous les navires du joueur sont coulés."""
        return all(navire.est_coule() for navire in self.navires)

