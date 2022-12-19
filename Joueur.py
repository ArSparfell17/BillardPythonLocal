
class Joueur:
    """Classe qui cractérise les différents joueurs

    faite par Hortense LEYNIER & Bérénice du BARET
    """
    def __init__(self, N = 0, nom ='Nameless' ):
        self.nom = nom
        self.N= N
        self.nb_points=0


    def __str__(self):
        return "Joueur", str(self.nom), "n°", str(self.N)

    @property
    def num(self):
        """
        coords: tuple
            Les coordonnées de la bille sur le plateau de jeu
        """
        return self.N