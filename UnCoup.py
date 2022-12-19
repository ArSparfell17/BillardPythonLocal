import numpy as np
import matplotlib.pyplot as p
import Deplacement as dep
import Plateau as plat
import Billes as bille


class UnCoup() :
    """Classe qui gère le dÃƒÂ©roulement d'un coup

    faite par Bérénice du BARET
    """
    def __init__(self, nb_billes):
        self.nb_billes = nb_billes


    def on_tire(self, plat):
        """
        Fonction qui permet de gérer le déroulé d'un coup

        Entrée
        - plat : le plateau

        Sortie :
        - le dictionnaire pos
        """

        # Initialisation des dictionaires qui vont recevoir les positions et vitesse des différentes billes à l'instant t
        pos = {}

        for ball in plat :
            pos["X" + str(ball.nombre)], pos["Y" + str(ball.nombre)], pos["Vt" + str(ball.nombre)], pos["Balles_touchées_par" + str(ball.nombre)] = [ball.coords[0]], [ball.coords[1]], [ball.vo], []

        # Mouvement de chaque bille par intervalle de temps :
        a = True
        while a == True:

            for ball in plat:

                i = ball.c  # récupération du numéro de la bille /!\commence à 1 et pas 0 !!!

                Xe, Ye, vo = ball.mouvement(pos)  # récupération des nouvelles coords de la bille

                # ajout des nouvelles coords et de la vitesse dans les dictionnaires adaptés
                pos["X" + i].append(Xe)
                pos["Y" + i].append(Ye)
                pos["Vt" + i].append(vo)

                #determination de la fin de la simulation si toutes les billes ont une vitesse nulle

                compte_vitesse = 0

                for ball in plat :

                    if np.linalg.norm(ball.vo) == 0:
                        compte_vitesse += 1  # si la bille est à "l'arret", alors le compteur augmente d'une itération

                # si le compteur note que TOUTES les billes sont à l'arret, il arrête la simulation
                if compte_vitesse == self.nb_billes:
                    print("balle arrêtée")
                    a = False

        #print des différentes billes touchées par qui
        for ball in plat :
            print("balles touchée par ", ball.c, " :", pos["Balles_touchées_par" + ball.c])

        return pos


    def point_gagnant(self, p, pos, nb_balles):
        """
        Fonction qui vérifie si le point est gagnant pour le joueur qui à tiré

        Entrée
        - p [int]: numéro du joueur qui tire
        - pos [dico]: le dictionnaire des billes
        - nb_balles [list]: nombres de balles présentes sur le plateau

        Sortie :
        - 1 si le joueur est gagnant
        - 0 sinon
        """

        print("je compte les points")
        test_balles = 0
        other_balls = [i for i in range(1,nb_balles+1)]
        other_balls.remove(p)

        #note le nombre de balles différentes dans la liste des balles touchées
        for i in other_balls:
            if i in pos["Balles_touchées_par" + str(p)] :
                test_balles +=1

        #si la balle en a touché au moins deux autres, alors elle marque un point
        if test_balles >= 2 :
            print("tu as marqué un point !")
            return True

        return False
