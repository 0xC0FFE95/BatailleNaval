class Navire:
    """
    Classe Navire
    ------------
    Représente un navire avec :
    - nom (str) : le type de navire (ex : "Porte-avions")
    - taille (int) : le nombre de cases occupées (ex : 5)
    - positions (list[tuple[int, int]]) : liste des coordonnées (row, col)
      où est placé le navire.
    - positions_touchees (list[tuple[int, int]]) : liste des cases
      du navire qui ont été touchées.

    La classe fournit :
    - la liste des navires disponibles (NAVIRES_DISPONIBLES)
    - une méthode est_coule() pour vérifier si toutes les positions
      ont été touchées.
    """
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
        self.positions = []           # Liste de (row, col)
        self.positions_touchees = []  # Cases où le navire a été touché

    def est_coule(self):
        """
        Retourne True si toutes les positions du navire
        sont touchées, c'est-à-dire si la longueur de
        positions_touchees == taille du navire.
        """
        return len(self.positions_touchees) == self.taille