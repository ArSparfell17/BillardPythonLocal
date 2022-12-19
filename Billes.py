
import numpy as np
import matplotlib.pyplot as p
import Plateau as cadre
import Deplacement as dep
import copy
from interface import *


class Billes:
    """Classe qui gère les différentes billes

    faite par Bérénice du BARET
    """
    def __init__(self, numero, Xe, Ye, plat, vo=np.array([0,0])) :
        self.nombre = numero #numéro de la boule
        self.__coords= Xe,Ye

        self.__vo = vo
        self.table = plat

        self.rayon = self.table.r

    def __str__(self):
        return self.x, self.y, self.vo

    def type(self):
        """
        Renvoie le numéro du propriétaire de la bille, et N si c'est la neutre.

        Paramètres : Aucun

        Renvoie : c : Le caractère représentant la bille

        """
        if self.nombre == 1 :
            print('suis là !')
            return '1'
        elif self.nombre == 2 :
            return '2'
        else :
            return 'N'

    @property
    def coords(self):
        """
        coords: tuple
            Les coordonnées de la bille sur le plateau de jeu
        """
        return self.__coords

    @property
    def x(self):
        """
        x: nombre entier
            Abscisse de la bille
        """
        return self.coords[0]

    @property
    def y(self):
        """
        y: nombre entier
            Ordonnée de la bille
        """
        return self.coords[1]

    @property
    def c(self):
        """
        y: nombre entier
            Ordonnée de la bille
        """
        return str(self.nombre)

    @property
    def vo(self):
        """
        vo: tableau array
            Vecteur vitesse de la bille
        """
        return self.__vo

    @vo.setter
    def vo(self, nouv_vo):
        """
        Met à jour la vitesse de la bille après un mouvement.
        Paramètres : les nouvelles vitesses de la bille
        """
        if np.linalg.norm(nouv_vo) < 2 :
            nouv_vo = np.array([0, 0])
        self.__vo= nouv_vo

    @coords.setter
    def coords(self, nouv_coords):
        """
        Met à jour les coordonnées de la bille après un mouvement.
        Paramètres : les nouvelles coordonnées de la bille
        """
        x, y = nouv_coords
        self.__coords = (x, y)




    def mouvement(self, pos):
        """
        Fonction qui gère le mouvement unitaire de la bille. Le mouvement qu'elle fait, si elle percute un mur ou pas et la définition de son vecteur vitesse

        Entrée
        - pos [dico]: le dictionnaire des billes

        Sortie :
        - X [int] : la nouvelle position de la bille en x
        - Y [int] : la nouvelle position de la bille en y
        - vo [tuple] : le nouveau vecteur vo de la bille
        """

        #calcul des nouvelles coordonnées grâce à la classe mouvement :

        dept = dep.Deplacement()
        (X_ancien, Y_ancien) = copy.deepcopy(self.coords)
        self.coords, self.vo = dept.mouvement_unitaire(self.x, self.y, self.vo)


        #print(self.c, '| x=', round(self.x, 3), '; y=', round(self.y, 3), '; vo =', self.vo)


        #on vérifie que les coordonées trouvées ne se trouvent pas dans un mur ou dans une balle.
        #Auquel cas il ne faut pas continuer, mais rebondir
        self.wall_or_not()

        vacetinstant = copy.deepcopy(self.vo)

        num_balle_touchee = self.ball_or_not(pos)

        #si deux balles sont en contact, on insufle à la balle touchée la vitesse initiale de l'autre bille avant l'impact
        if num_balle_touchee != False :
            self.coords = (X_ancien, Y_ancien) #on reprend l'itération précédente pour éloigner la balle

            for ball in self.table :
                if ball.nombre == num_balle_touchee :
                    self.vo = self.vo * 0.7
                    ball.vo = vacetinstant * 0.7

            #on met à jour le dictionnaire pour garder un oeil sur quelle balles à touchée qui pour le décompte final de spoints
            pos["Balles_touchées_par" + self.c].append(num_balle_touchee)
            pos["Balles_touchées_par" + str(num_balle_touchee)].append(self.nombre)
            #print('---------balle touchée :', num_balle_touchee, '---- v donné', vacetinstant,'-----------------')

        return (self.x, self.y, self.vo)

    def un_pas(self, pos, iteration):
        """
        Fonction qui gère le mouvement unitaire de la bille. Le mouvement qu'elle fait, si elle percute un mur ou pas et la définition de son vecteur vitesse

        Entrée
        - pos [dico]: le dictionnaire des billes
        - interation [int]: le numéro de l'iteration

        """
        x, y = pos['X'+self.c][iteration], pos['Y'+self.c][iteration]
        self.__coords = x, y


    def wall_or_not(self):
        """
        Fonction qui vérifie si la balle pércute un mur ou pas

        """

        rballe=self.rayon

        L = 1011  #valeurs expérimentales
        l = 545

        if self.x<=rballe - 55 :
            #print('on a tapé le = Left')
            self.coords = rballe - 55, self.y
            self.vo[0] = -self.vo[0]

        elif self.x>=L - rballe :
            #print('on a tapé le = Right')
            self.coords = L - rballe, self.y
            self.vo[0] = -self.vo[0]

        elif self.y<=rballe - 33 :
            #print('on a tapé le = Bottom ')
            self.coords = self.x, rballe - 33
            self.vo[1] = -self.vo[1]

        elif self.y>=l - rballe :
            #print('on a tapé le = Top')
            self.coords = self.x, l-rballe
            self.vo[1] = -self.vo[1]

        else :
            pass

    def ball_or_not(self, pos):
        """
        Fonction qui vérifie si la balle pércute une autre balle ou pas
        Entrée
        - pos [dico]: le dictionnaire des billes

        Sortie :
        - [int] : la bille tapée en cas de contact
        - False : sinon
        """
        x, y = self.x, self.y
        rballe = self.rayon/2


        for autre_ball in range(1, self.table.nb + 1):
            if autre_ball == self.nombre :
                pass
            else:

                Xb = pos["X" + str(autre_ball)][-1]
                Yb = pos["Y" + str(autre_ball)][-1]

                # si la balle est a portée d'une balle ennemie :

                if ((x - Xb)**2 + (y-Yb)**2)**(1/2) <= 2*rballe :

                    mu = (self.rayon/2 - self.table.epsilon)

                    # alors on vérifie dans quel sens elle doit repartir
                    if x <= Xb and Yb - mu <= y <= Yb + mu:
                        # print('on a tapé la balle à Right')
                        self.vo[0] = -self.vo[0]
                        return autre_ball

                    elif Xb <= x and Yb - mu <= y <= Yb + mu:
                        #print('on a tapé la balle à Left')
                        self.vo[0] = -self.vo[0]
                        return autre_ball

                    elif Xb - mu <= x <= Xb + mu and Yb <= y :
                        #print('on a tapé la balle à Top')
                        self.vo[1] = -self.vo[1]
                        return autre_ball

                    elif Xb - mu <= x <= Xb + mu and y <= Yb:
                        #print('on a tapé le = Bottom ')
                        self.vo[1] = -self.vo[1]
                        return autre_ball

                    # si la balle tape un des coins de la balle
                    elif (x< Xb -mu and y< Yb - mu) or (x> Xb+mu and y< Yb - mu) or (x< Xb -mu and y>Yb+mu ) or (x> Xb+mu and y>Yb+mu ) :
                        # print('on a tapé le = Koin ')
                        self.vo[0], self.vo[1] = self.vo[1], self.vo[0]  # le vecteur s'inverse totalement
                        return autre_ball

        # si la balle n'a rien tapé du tout
        return False

#classe fille des différentes balles pour l'affichage de l'IHM
class Bille_1(Billes):
    def car(self):
        return 'B1'

class Bille_2(Billes):
    def car(self):
        return 'B2'

class Bille_n(Billes):
    def car(self):
        return 'BN'