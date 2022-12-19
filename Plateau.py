#import numpy as np
import matplotlib.pyplot as p
import random as rd
import Billes as b


class Plateau(list):
    """Classe qui stocke le plateau et les billes qui sont dessus

    faite par Bérénice du BARET
    """
    def __init__(self, Longueur, largeur, nb_billes = 3, r_ball = 35, epsilon = 10):
        self.L = Longueur
        self.l = largeur
        self.r = r_ball
        self.epsilon = epsilon
        self.nb = nb_billes

        #création des billes
        bille_1 = b.Bille_1(1, 200, 400, self)
        bille_2 = b.Bille_2(2, 200, 100, self)
        self.append(bille_1)
        self.append(bille_2)
        for k in range(3, nb_billes+1):
            bille_n = self.generation_bille_neutre(k)
            self.append(bille_n)



    def __len__(self):
        return self.nb

    def __str__(self):
        return "le plateau est aux dimmentions : {} cm par {}".format(self.L, self.l)

    def generation_bille_neutre(self, k):
        """
        Fonction qui génère les balles neutres en fonction des balles déjà présentes sur le plateau

        Entrée
        - k [int]: numéro du joueur qui tire


        Sortie :
        - 1 si le joueur est gagnant
        - 0 sinon
        """
        #crée une bille
        bille_n = b.Bille_n(k, rd.randint(1, 900), rd.randint(1, 500), self)

        #vérifie que la bille ne chevauche pas une bille déjà existante, auquel cas il recommence la fonction
        for balle in self:
            if ((bille_n.x - balle.x) ** 2 + (bille_n.y - balle.y) ** 2) ** (1 / 2) <= 2*bille_n.rayon :
                bille_n = self.generation_bille_neutre(k)
        return bille_n



