import unittest
from rommee_backend import *

#calc_area_value
class TestAreaPointsCalculation(unittest.TestCase):

    def test_simpleCount_1r_1g_1b(self):
        area = [Stone(1, Color.RED), Stone(1, Color.GREEN), Stone(1, Color.BLUE)]
        self.assertEqual(75,calc_area_value(area), "1r_1g_1b")

    def test_simpleCount_j_1g_1b(self):
        area = [Stone(0, Color.JOKER), Stone(1, Color.GREEN), Stone(1, Color.BLUE)]
        self.assertEqual(75,calc_area_value(area), "j_1g_1b")

    def test_simpleCount_1r_j_1b(self):
        area = [Stone(1, Color.GREEN),Stone(0, Color.JOKER), Stone(1, Color.BLUE)]
        self.assertEqual(75,calc_area_value(area), "1g_j_1b")

    def test_simpleCount_1r_1g_j(self):
        area = [Stone(1, Color.GREEN), Stone(1, Color.BLUE),Stone(0, Color.JOKER)]
        self.assertEqual(75,calc_area_value(area), "1g_1b_j")

    def test_simpleCount_1r_2r_3r(self):
        area = [Stone(1, Color.RED), Stone(2, Color.RED), Stone(3, Color.RED)]
        self.assertEqual(6,calc_area_value(area), "1r_2r_3r")

    def test_simpleCount_1r_2r_j(self):
        area = [Stone(1, Color.RED), Stone(2, Color.RED), Stone(0, Color.JOKER)]
        self.assertEqual(6,calc_area_value(area), "1r_2r_j")

    def test_simpleCount_1r_j_3r(self):
        area = [Stone(1, Color.RED), Stone(0, Color.JOKER), Stone(3, Color.RED)]
        self.assertEqual(6,calc_area_value(area), "1r_j_3r")

    def test_simpleCount_j_2r_3r(self):
        area = [Stone(0, Color.JOKER), Stone(2, Color.RED), Stone(3, Color.RED)]
        self.assertEqual(6,calc_area_value(area), "j_2r_3r")

    def test_simpleCount_9r_10r_11r(self):
        area = [Stone(9, Color.RED), Stone(10, Color.RED), Stone(11, Color.RED)]
        self.assertEqual(30,calc_area_value(area), "9r_10r_11r")

    def test_simpleCount_9r_10r_j(self):
        area = [Stone(9, Color.RED), Stone(10, Color.RED), Stone(0, Color.JOKER)]
        self.assertEqual(30,calc_area_value(area), "9r_10r_j")

    def test_simpleCount_9r_10r_j(self):
        area = [Stone(8, Color.RED),Stone(0, Color.JOKER), Stone(10, Color.RED), Stone(0, Color.JOKER)]
        self.assertEqual(38,calc_area_value(area), "8r_j_10r_j")

    def test_simpleCount_12r_13r_1r(self):
        area = [Stone(12, Color.RED), Stone(13, Color.RED), Stone(1, Color.RED)]
        self.assertEqual(39,calc_area_value(area), "12r_13r_1r")

    def test_simpleCount_11r_12r_j_1(self):
        area = [Stone(11, Color.RED), Stone(12, Color.RED), Stone(0, Color.JOKER), Stone(1, Color.RED)]
        self.assertEqual(50,calc_area_value(area), "11r_12r_j_1r")

    def test_simpleCount_12r_13r_j(self):
        area = [Stone(12, Color.RED), Stone(13, Color.RED), Stone(0, Color.JOKER)]
        self.assertEqual(39,calc_area_value(area), "12r_13r_j")

    def test_simpleCount_11r_11g_11b(self):
        area = [Stone(11, Color.RED), Stone(11, Color.GREEN), Stone(11, Color.BLUE)]
        self.assertEqual(33,calc_area_value(area), "11r_11g_11b")

    def test_simpleCount_5r_5g_5b(self):
        area = [Stone(5, Color.RED), Stone(5, Color.GREEN), Stone(5, Color.BLUE)]
        self.assertEqual(15,calc_area_value(area), "5r_5g_5b")


if __name__ == '__main__':
    unittest.main()
