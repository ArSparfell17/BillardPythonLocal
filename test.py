from Billes import *
from Plateau import *
from UnCoup import *
import Joueur
import unittest
import numpy as np


class Test(unittest.TestCase):
    """Classe qui assure les différents tests unitaires

    faite par Hortense LEYNIER
    """
    def test_billes(self):
        table = Plateau(1000,500)
        b1 = table[0]
        b2 = table[1]
        b3 = table[2]
        self.assertIsInstance(b1,Billes)
        self.assertEqual(b2.nombre, 2)

    def test_coords(self):
        table = Plateau(1000, 500)
        for bille in table:
            self.assertTrue(bille.coords[0]< table.L and bille.coords[0] > 0)
            self.assertTrue(bille.coords[1] < table.l and bille.coords[1] > 0)

    def test_deplacement(self):
        table = Plateau(1000, 500)
        coup = UnCoup(table.nb)
        table[0].vo = np.array((20,4))
        coup.on_tire(table)
        for bille in table:
            self.assertTrue(bille.coords[0]< table.L)
            self.assertTrue(bille.coords[1] < table.L)


    def test_type(self):
        table = Plateau(1000, 500)
        coup = UnCoup(table.nb)
        table[0].vo = np.array((20,4))
        dic = coup.on_tire(table)

        self.assertIsInstance(table, list)
        self.assertIsInstance(dic, dict)




if __name__ == '__main__':
    unittest.main()