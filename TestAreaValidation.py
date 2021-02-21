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

    def test_simpleStoneVariant_1b_2b_3b(self):
        area = [Stone(1,Color.BLUE), Stone(2,Color.BLUE),Stone(3,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"1b_2b_3b")

    def test_simpleStoneVariant_1b_2b_2b_3b(self):
        area = [Stone(1,Color.BLUE), Stone(2,Color.BLUE),Stone(2,Color.BLUE),Stone(3,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertFalse(validate_area_stone_constellation(area),"1b_2b_2b_3b")

    def test_simpleStoneVariant_1b_2b_4b_3b(self):
        area = [Stone(1,Color.BLUE), Stone(2,Color.BLUE),Stone(4,Color.BLUE),Stone(3,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertFalse(validate_area_stone_constellation(area),"1b_2b_4b_3b")

    def test_stoneVariant_12b_13b_1b(self):
        area = [Stone(12,Color.BLUE), Stone(13,Color.BLUE),Stone(1,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"12b_13b_1b")

    def test_stoneVariant_12b_j_1b(self):
        area = [Stone(12,Color.BLUE), Stone(0,Color.JOKER),Stone(1,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"12b_j_1b")

    def test_stoneVariant_2b_6b_7b(self):
        area = [Stone(2,Color.BLUE), Stone(6,Color.BLUE),Stone(7,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertFalse(validate_area_stone_constellation(area),"2b_6b_7b")

    def test_stoneVariant_6b_7b(self):
        area = [Stone(6,Color.BLUE),Stone(7,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertFalse(validate_area_stone_constellation(area),"6b_7b")

    def test_stoneVariant_j_13b_1b(self):
        area = [Stone(0,Color.JOKER),Stone(13,Color.BLUE),Stone(1,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"j_13b_1b")

    def test_stoneVariant_j_8g_8b(self):
        area = [Stone(0,Color.JOKER),Stone(8,Color.GREEN),Stone(8,Color.BLACK)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"j_8g_8black")

    def test_stoneVariant_8g_j_8b(self):
        area = [Stone(8,Color.GREEN),Stone(0,Color.JOKER),Stone(8,Color.BLACK)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"8g_j_8black")

    def test_stoneVariant_8g_8b_j(self):
        area = [Stone(8,Color.GREEN),Stone(8,Color.BLACK),Stone(0,Color.JOKER)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"8g_8black_j")

    def test_stoneVariant_8b_8g_j(self):
        area = [Stone(8,Color.BLACK),Stone(8,Color.GREEN),Stone(0,Color.JOKER)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"8black_8g_j")

    def test_simpleStoneVariant_4b_5b_6b_7b_8b_9b_10b(self):
        area = [Stone(4,Color.BLUE), Stone(5,Color.BLUE),Stone(6,Color.BLUE),Stone(7,Color.BLUE),Stone(8,Color.BLUE),Stone(9,Color.BLUE),Stone(10,Color.BLUE)]
        validate_area_stone_constellation(area)
        self.assertTrue(validate_area_stone_constellation(area),"4b_5b_6b_7b_8b_9b_10b")





if __name__ == '__main__':
    unittest.main()