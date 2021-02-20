import unittest
from rommee_backend import *

class TestAreaValidation(unittest.TestCase):
    def test_simpleStoneVariant_5r_5g_5b(self):
        area = [Stone(5,Color.RED), Stone(5,Color.GREEN),Stone(5,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"5r_5g_5b")

    def test_simpleStoneVariant_5r_6g_5b(self):
        area = [Stone(5,Color.RED), Stone(6,Color.GREEN),Stone(5,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertFalse(validate_area_stone_constellation(area),"5r_6g_5b")

    def test_simpleStoneVariant_5r_5r_5b(self):
        area = [Stone(5,Color.RED), Stone(5,Color.RED),Stone(5,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertFalse(validate_area_stone_constellation(area),"5r_5r_5b")

    def test_simpleStoneVariant_5r_5b_5r(self):
        area = [Stone(5,Color.RED), Stone(5,Color.BLUE),Stone(5,Color.RED)]
        validate_area_stone_constellation(area)
        self.assertFalse(validate_area_stone_constellation(area),"5r_5b_5r")

    def test_simpleStoneVariant_j_5b_5r(self):
        area = [Stone(0,Color.JOKER), Stone(5,Color.BLUE),Stone(5,Color.RED)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"j_5b_5r")

    def test_simpleStoneVariant_j_5b_5r_j(self):
        area = [Stone(0,Color.JOKER), Stone(5,Color.BLUE),Stone(5,Color.RED),Stone(0,Color.JOKER)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"j_5b_5r_j")

    def test_simpleStoneVariant_4b_5b_6b(self):
        area = [Stone(4,Color.BLUE), Stone(5,Color.BLUE),Stone(6,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"4b_5b_6b")





if __name__ == '__main__':
    unittest.main()