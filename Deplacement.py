
import numpy as np
import matplotlib.pyplot as p
import Plateau as cadre
from interface import *


class Deplacement():
    """Classe qui assure le déplacement des billes

    faite par Bérénice du BARET
    """
    def __init__(self):
        m = 50  # (g) masse de la bille
        f = 0.9 # coefficient de frottement
        h = 0.1  # (s) le pas de temps

        self.coeff = -f/m
        self.h = h

    def acceleration(self, v):
        """
        Retourne la dérivée du vecteur vitesse

        Entrée
            v [1D array] : vecteur vitesse
        """
        vdot = self.coeff*v
        return vdot


    def mouvement_unitaire(self, x, y, vo):
        """
        Fonction qui gère le mouvement théorique, renvoyant les nouvelles positions de la balle selon la méthode d'Euler

        Entrée
        - x, y [int] : position de la balle avant le mouvement
        - vo [tuple]: vecteur vo imposée à la balle

        Sortie :
        - coords [tuple] : les nouvelles coordonnées d'après la méthode d'Euler
        - vo [tuple] : le nouveau vecteur vitesse d'après la méthode d'Euler
        """
        #Nouveau Vo
        vo = vo + self.h * self.acceleration(vo)

        # projection sur les axes x et y
        Xe = vo[0] * 0.05 + x
        Ye = vo[1] * 0.05 + y
        coords = Xe, Ye
        return (coords, vo)



    def mouvement_droit(self, X, Y, vtot, v, other_ball, i, plat):
        """
        Fonction qui permettait de gérer le mouvement entier d'une balle. Fonction remplacée par le mouvement unitaire, plus simple à manipuler et à gérer
        """

        # on retrouve les valeurs v0 et la position de la balle
        vo = v[-1]
        pos = (X[-1], Y[-1])
        print('on enlève 2 à 1', other_ball, '/', pos)
        other_ball.remove(pos)
        print('les autres balles sont à :', other_ball)
        i = 1
        while True:
            # euler
            vo = vo + self.h * deplacement.acceleration(self, vo)
            vtot.append((vo[0]**2+vo[1]**2)**(1/2))
            v.append(vo)
            # projection of the pendulum on the X/Y axis
            Xe = vo[0]*i*0.05 + pos[0]
            Ye = vo[1]*i*0.05 + pos[1]

            print(round(vtot[-1], 2), '/', 0.5, '; x=', round(Xe, 3), '; y=', round(Ye, 3), '; vo =', v[-1])

            #on vérifie que les coordonées trouvées ne se trouvent pas dans un mur ou dans une balle. Auquel cas il ne faut pas continuer, mais rebondir
            wall = plat.wall_or_not(Xe, Ye)
            if wall == True :
                wall = plat.ball_or_not(Xe, Ye, i, other_ball)

            #Condition pour sortir de la boucle de la trajectoire en ligne droite :
                #Si la balle percute un mur :
            if wall != True :
                print('on a tapé le =', wall)
                other_ball.append((X[-1], Y[-1]))
                return (X, Y, vtot, v, wall)

                #Si la vitesse est trop lente
            if vtot[-1] <= 0.5 :
                wall = 'Stop'
                other_ball.append((X[-1], Y[-1]))
                return (X, Y, vtot, v, wall)

            # store the current state vector
            X.append(Xe)
            Y.append(Ye)
            i+= 1



    def plot_position(self, Y, X, Longueur, largeur, other_ball, titre) :
        """
        Affiche la position finale et la trajectoire d'une bille
        """

        # realtime eye candy pendulum drawing
        p.figure()
        Xb, Yb = [], []

        p.plot(X,Y, color="red", label="balle")
        for o_b in other_ball :
            Xb.append(o_b[0])
            Yb.append(o_b[1])
        p.plot(Xb, Yb, 'bo', label='position finale balles')
        p.xlabel("Axe X (cm)")
        p.ylabel("Axe Y (cm)")
        p.title(titre)

        p.legend()
        p.xlim((0, Longueur))
        p.ylim((0, largeur))

    def plot_speed(self, vtot):
        """
        Affiche les vitesses d'une certaine balle au cours du temps
        """

        p.plot(vtot, 'b', label="speed")
        p.xlabel("Temps")
        p.ylabel("Vitesse")
        p.title("Vitesse en fonction du temps")
        p.legend()
        p.grid(True)

    def plot_position_all(self, pos, nb_balles, Longueur, largeur, legend) :
        """
        Affiche les positions initiales et finale de toutes les balles ainsi que leur trajectoire
        """

        p.figure()
        X_dep, Y_dep = [], []
        X_arr, Y_arr = [], []

        for i in range(1, nb_balles +1) :
            p.plot(pos["X" + str(i)],pos["Y" + str(i)], label="balle "+str(i))
            X_dep.append(pos["X" + str(i)][0])
            Y_dep.append(pos["Y" + str(i)][0])

            X_arr.append(pos["X" + str(i)][-1])
            Y_arr.append(pos["Y" + str(i)][-1])


        p.plot(X_dep, Y_dep, 'ro', label='position initiale balles')
        p.plot(X_arr, Y_arr, 'bo', label='position finale balles')
        p.xlabel("Axe X (cm)")
        p.ylabel("Axe Y (cm)")
        p.title(legend)

        p.legend()
        p.xlim((0, Longueur))
        p.ylim((0, largeur))


