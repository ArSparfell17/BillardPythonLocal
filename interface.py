# -*- coding: utf-8 -*-
import sys
from Plateau import *
from Joueur import *
from Billes import *
from UnCoup import *

from random import shuffle

from PyQt5 import QtGui, QtCore, QtWidgets, uic
import numpy as np
from PyQt5.QtWidgets import QMessageBox


class BillardUI(QtWidgets.QMainWindow):
    def __init__(self,nb_boule=3, *args):

        #définition des variables de la classe :
        self.nbboule = nb_boule
        self.joueur_actif = 1
        self.deja_enregistrer = 0

        #Création de l'écran de jeu :
        QtWidgets.QMainWindow.__init__(self, *args)
        self.ui = uic.loadUi('interface3.ui', self)
        pixmap = QtGui.QPixmap("image_plateau.png")
        pixmap_resized = pixmap.scaled(1111, 611, QtCore.Qt.IgnoreAspectRatio)
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap_resized))
        self.ui.conteneur.lower()
        self.ui.conteneur.stackUnder(self)
        self.ui.conteneur.setAutoFillBackground(True)
        self.ui.conteneur.setPalette(pal)
        self.table = None

        self.painter = QtGui.QPainter()
        self.img_dict = {}

        self.generer()


        self.ui.conteneur.paintEvent = self.draw_table

        #Initialisation du timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.un_pas_simulation)



        #gestion des différents boutons qui constituent le menu :
        self.labelj1 = QtWidgets.QLabel(self)
        self.labelj1.setText("Nom du joueur 1 = {0}\n\nNombre de point = {1}".format(self.joueur1.nom, self.joueur1.nb_points))
        self.labelj1.move(50, 720)
        self.labelj1.adjustSize()

        self.labelj2 = QtWidgets.QLabel(self)
        self.labelj2.setText("Nom du joueur 2 = {0}\n\nNombre de point = {1}".format(self.joueur2.nom, self.joueur2.nb_points))
        self.labelj2.move(900, 720)
        self.labelj2.adjustSize()

        self.label_actif = QtWidgets.QLabel(self)
        self.label_actif.setText('Au tour de :\n {0}'.format(self.joueur1.nom))
        self.label_actif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_actif.move(535, 733)
        self.label_actif.adjustSize()

        self.b0 = QtWidgets.QPushButton(self)
        self.b0.setText('Commencer la partie')
        self.b0.move(500, 700)
        self.b0.adjustSize()

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Charger une partie')
        self.b1.move(505, 750)
        self.b1.adjustSize()

        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setText('Sauvegarder')
        self.b3.move(435, 733)
        self.b3.adjustSize()
        self.b3.setHidden(True)

        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setText('Quitter')
        self.b4.move(635, 733)
        self.b4.adjustSize()
        self.b4.setHidden(True)
        self.label_actif.setHidden(True)

        self.b0.clicked.connect(self.nvlle_partie)
        self.b1.clicked.connect(self.charger_partie)
        self.b3.clicked.connect(self.sauvegarder)
        self.b4.clicked.connect(self.close)

    def draw_table(self, *args):
        """Créé et depose les billes sur le plateau de l'IHM
        """
        # on informe le peintre qu'on veut dessiner dans le widget conteneur
        self.painter.begin(self.ui.conteneur)
        # variable intermédiraire pour alléger le code
        qp = self.painter

        # boucle pour parcourir les insectes et gérer les images (vu ci-dessus)
        for bille in self.table:
            cls_name = bille.__class__.__name__
            if cls_name not in self.img_dict:
                # il faut avoir dans le répertoire les images qui portent le nom
                # de la classe
                image_bille = QtGui.QImage(cls_name + ".png")
                image_bille_scaled = image_bille.scaled(100, 100, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)

                self.img_dict[cls_name] = image_bille_scaled  # cls_name + ".png")
            img = self.img_dict[cls_name]
            # on demande au peintre d'afficher l'image aux coordonnées de l'insecte
            if type(bille.coords[0]) == np.ndarray:
                self.bille.coords[0] = self.bille.coords[0][0]
            if type(bille.coords[1]) == np.ndarray:
                self.bille.coords[1] = self.bille.coords[1][0]

            qp.drawImage(bille.coords[0], bille.coords[1], img)

        # on informe le peintre qu'on a fini
        self.painter.end()

    def generer(self):
        """
        Génère le plateau et initie les joueurs

        faite par Bérénice du BARET
        """

        # Initialisation du plateau contenanant les billes :
        plat = Plateau(self.ui.conteneur.height(), self.ui.conteneur.width(), self.nbboule)
        self.table = plat
        self.conteneur.update()

        # Initialisation des joueurs
        self.joueur1 = Joueur(1)
        self.joueur2 = Joueur(2)

        self.coup = UnCoup(self.nbboule)

        # création du dictionnaire pos qui permet de stocker le mouvement des billes à chaque instant du mouvement.
        # Ce dictionnaire ne sert que pour sauvegarder une partie si aucune boule n'a été tirée, autrement, il est réinisialisé à chaque coup
        self.pos = {}
        for ball in self.table:
            self.pos["X" + str(ball.nombre)], self.pos["Y" + str(ball.nombre)], self.pos["Vt" + str(ball.nombre)], \
            self.pos["Balles_touchées_par" + str(ball.nombre)] = [ball.coords[0]], [ball.coords[1]], [ball.vo], []

    def nvlle_partie(self):
        """
        Fonction qui permet de lancer une nouvelle partie

        faite par Hortense LEYNIER

        """

        nom = QtWidgets.QInputDialog(self)
        n1, ok = nom.getText(self, "Nom des joueurs", "Entrer le nom du joueur 1")
        if ok:
            if len(n1)!=0 :
                self.joueur1.nom = n1
        n2, ok = nom.getText(self, "Nom des joueurs", "Entrer le nom du joueur 2")
        if ok:
            if len(n2) != 0:
                self.joueur2.nom = n2

        self.label_actif.setText('Au tour de :\n {0}'.format(self.joueur1.nom))
        self.label_actif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_actif.adjustSize()
        self.label_actif.update()

        #Initialisation des points des joueurs utiles en cas de nouvelle partie après avoir atteint 300 points
        self.joueur1.nb_points = 0
        self.joueur2.nb_points = 0
        self.deja_enregistrer = 0

        #affichage des textes
        self.labelj1.setText("Nom du joueur 1 = {0}\n\nNombre de point = {1}".format(self.joueur1.nom, self.joueur1.nb_points))
        self.labelj2.setText("Nom du joueur 2 = {0}\n\nNombre de point = {1}".format(self.joueur2.nom, self.joueur2.nb_points))
        self.labelj2.adjustSize()
        self.labelj1.adjustSize()
        self.labelj1.update()
        self.labelj2.update()


        self.b0.close()
        self.b1.close()
        self.b3.setHidden(False)
        self.b4.setHidden(False)
        self.label_actif.setHidden(False)

    def charger_partie(self):
        """
        Fonction qui permet de charger une partie à partir d'un fichier texte existant

        faite par Hortense LEYNIER

        """

        item = QtWidgets.QFileDialog(self, caption='Choisi un fichier')
        file = item.getOpenFileNames()
        self.deja_enregistrer = 1

        txt = open(str(file[0][0]),'r')
        f = []
        for line in txt :
            f.append(line)

        self.joueur1.nom=f[-5]
        self.joueur2.nom=f[-4]

        self.joueur1.nb_points = int(f[-3])
        self.joueur2.nb_points = int(f[-2])
        self.joueur_actif = int(f[-1])

        self.nbboule = len(f) - 5
        plat = Plateau(self.ui.conteneur.height(), self.ui.conteneur.width(), self.nbboule)
        self.table = plat


        for balle in self.table:
            temp = f[balle.nombre-1].split(' ')
            balle.coords = float(temp[0]), float(temp[1])

        self.ui.conteneur.update()


        self.labelj1.setText("Nom du joueur 1 = {0}\n\nNombre de point = {1}".format(self.joueur1.nom, self.joueur1.nb_points))
        self.labelj1.move(50, 720)
        self.labelj1.adjustSize()

        self.labelj2.setText("Nom du joueur 2 = {0}\n\nNombre de point = {1}".format(self.joueur2.nom, self.joueur2.nb_points))
        self.labelj2.move(900, 720)
        self.labelj2.adjustSize()

        nom_actif = 'Nameless'
        if self.joueur_actif == 1 :
            nom_actif = self.joueur1.nom
        elif self.joueur_actif == 2 :
            nom_actif = self.joueur2.nom

        self.label_actif.setText('Au tour de :\n {0}'.format(nom_actif))
        self.label_actif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_actif.adjustSize()
        self.label_actif.update()

        self.b1.close()
        self.b0.close()
        self.b3.setHidden(False)
        self.b4.setHidden(False)

        self.label_actif.setHidden(False)

    def mousePressEvent(self, event):
        """
        Se lance au clic et permet de repérer la position du curseur sur le plateau

        faite par Bérénice du BARET
        """
        print("Un des joueurs à cliqué, rien ne va plus")
        y_clic = event.y()
        x_clic = event.x()

        self.tour_joueur(x_clic, y_clic)

    def sauvegarder(self):
        """
        Fonction qui gère l'enregistrement des parties et l'écriture des données importantes sur un fichier texte

        faite par Hortense LEYNIER

        """

        n = ''
        if self.deja_enregistrer == 1:
            nomf = QtWidgets.QFileDialog(self, caption='Enregister la partie')
            nom = nomf.getSaveFileUrl()
            print("n = ", nom)
            n = nom[1][1]
        if self.deja_enregistrer == 0:
            no = QtWidgets.QInputDialog(self)
            n, ok = no.getText(self, "Sauvegarde de la partie", "Nom de la partie")
            if ok:
                self.deja_enregistrer = 1

        if len(n) == 0 :
            n = self.joueur1.nom + '_' + self.joueur2.nom

        txt = open(n + '.txt', 'w')
        for i in range(1, len(self.table)+1):
            txt.write(str(self.pos['X' + str(i)][-1]))
            txt.write(' ')
            txt.write(str(self.pos['Y' + str(i)][-1]))
            txt.write('\n')
        txt.write(str(self.joueur1.nom))
        txt.write('\n')
        txt.write(str(self.joueur2.nom))
        txt.write('\n')
        txt.write(str(self.joueur1.nb_points))
        txt.write('\n')
        txt.write(str(self.joueur2.nb_points))
        txt.write('\n')
        txt.write(str(self.joueur_actif))

    def tour_joueur(self,x_clic, y_clic):
        """
        Gère le calcul du tour et les différentes fonctions liées au calcul des points. Il se lance au clic sur le plateau.
        Il uptade le dictionnaire "pos" et lance le timer pour la simulation

        Entrée :
        x_clic, y_clic : position des clics sur le plateau

        faite par Bérénice du BARET
        """
        print("début du tour")

        #initialise le vecteur vitesse de la balle tirée
        for bille in self.table :
            if bille.nombre==self.joueur_actif:
                xe, ye = bille.coords
                bille.vo=np.array([(xe - (x_clic-90))*0.7, (ye - (y_clic-85))*0.7])

        print("on lance la procédure")
        self.pos = self.coup.on_tire(self.table)
        print("le coup à marché !")

        self.calcul_des_points(self.joueur_actif)

        self.timer.start(10)
        self.iteration = 0

    def un_pas_simulation(self):
        """
        Effectue la simulation d'un mouvement unitaire de chaque balle sur le plateau
        Il se lance à chaque timeout du timer

        faite par Bérénice du BARET
        """
        #Vérfie qu'il reste au moins une itération pour les billes
        if self.iteration == len(self.pos['X1']) :
            self.timer.stop()
            print('fin de la simulation')

        #si c'est la cas, déplace les balles d'une itération et met l'IHM à jour
        else :
            for bille in self.table:
                #print(bille.nombre, '| old |', bille.coords[0], bille.coords[1])
                bille.un_pas(self.pos, self.iteration)
                #print(bille.nombre, '| new |', bille.coords[0], bille.coords[1])

                self.ui.conteneur.update()
            self.iteration += 1


    def calcul_des_points(self, p) :
        """
        Permet le calcul des points à la fin de chaque tour.
        Il update les points de chaque joueur et le joueur actif à la fin du tour.

        Entrée :
        p : numéro du joueur qui a tiré ce coup-ci

        faite par Bérénice du BARET
        """
        #Vérifie si le point est gagnant
        temp = self.coup.point_gagnant(p, self.pos, self.nbboule)

        #Adapte les points des joueurs et le joueur actif en fonction
        if temp and p ==1:
            self.joueur1.nb_points+=1
            self.joueur_actif = 1
        elif temp and p == 2:
            self.joueur2.nb_points += 1
            self.joueur_actif = 2
        elif p ==1 :
            self.joueur_actif = 2
            print("joueur actif = 2 !!!! ")
        elif p ==2 :
            self.joueur_actif = 1

        # Arrête la partie si l'un des joueurs atteind le nombre max des point
        if max(self.joueur1.nb_points, self.joueur2.nb_points) == 300:
            self.fin_de_partie()

        #Met à jour les textes affichés à l'écran
        self.labelj1.setText("Nom du joueur 1 = {0}\n\nNombre de point = {1}".format(self.joueur1.nom, self.joueur1.nb_points))
        self.labelj1.adjustSize()
        self.labelj1.update()

        self.labelj2.setText("Nom du joueur 2 = {0}\n\nNombre de point = {1}".format(self.joueur2.nom, self.joueur2.nb_points))
        self.labelj2.adjustSize()
        self.labelj2.update()


        nom_actif = 'Nameless'
        if self.joueur_actif == 1 :
            nom_actif = self.joueur1.nom
            print("nom actif =", nom_actif)
        elif self.joueur_actif == 2 :
            nom_actif = self.joueur2.nom
            print("nom actif =",nom_actif)

        self.label_actif.setText('Au tour de :\n {0}'.format(nom_actif))
        self.label_actif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_actif.adjustSize()
        self.label_actif.update()

    def fin_de_partie(self):
        """
        Permet de vérifier si les joueurs ont "enfin" fini la partie

        faite par Hortense LEYNIER

        """
        gagnant = self.joueur1.nom
        if self.joueur1.nb_points < self.joueur2.nb_points:
            gagnant = self.joueur2.nom

        fin = QtWidgets.QMessageBox(self)
        fin.setWindowTitle('Fin de la partie')
        fin.setText('Bravo à {0}, tu as gagné la partie! Une nouvelle partie ?'.format(gagnant))
        fin.show()

        self.b3.setHidden(True)
        self.b4.setHidden(True)
        self.label_actif.setHidden(True)

        self.b0 = QtWidgets.QPushButton(self)
        self.b0.setText('Rejouer')
        self.b0.move(500, 700)
        self.b0.adjustSize()
        self.b0.setHidden(False)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Charger une partie')
        self.b1.move(495, 750)
        self.b1.adjustSize()
        self.b1.setHidden(False)

        self.b0.clicked.connect(self.nvlle_partie)
        self.b1.clicked.connect(self.charger_partie)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BillardUI()
    window.show()
    sys.exit(app.exec_())
