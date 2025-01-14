class Navire:
    """
    Représente un navire avec un nom, une taille,
    ses positions (liste de tuples de coordonnées),
    et un état (touché ou coulé).
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
        """Retourne True si toutes les positions sont touchées."""
        return len(self.positions_touchees) == self.taille
