import unittest
from rommee_backend import *

class TestStoneValueCalculation(unittest.TestCase):
    def test_simpleStoneVariant_x_6_7(self):
        testStone = Stone(5,Color.RED)
        area = [testStone, Stone(6,Color.RED),Stone(7,Color.RED)]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="x_6_7")

    def test_simpleStoneVariant_5_x_7(self):
        testStone = Stone(6,Color.RED)
        area = [Stone(5,Color.RED),testStone,Stone(7,Color.RED)]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="5_x_7")

    def test_simpleStoneVariant_5_6_x(self):
        testStone = Stone(7,Color.RED)
        area = [Stone(5,Color.RED),Stone(6,Color.RED),testStone]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="5_6_x")

    def test_simpleStoneVariant_x_11_12(self):
        testStone = Stone(10,Color.RED)
        area = [testStone, Stone(11,Color.RED),Stone(12,Color.RED)]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="x_11_12")

    def test_simpleStoneVariant_10_x_12(self):
        testStone = Stone(11,Color.RED)
        area = [Stone(10,Color.RED),testStone,Stone(712,Color.RED)]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="10_x_12")

    def test_simpleStoneVariant_10_11_x(self):
        testStone = Stone(12,Color.RED)
        area = [Stone(10,Color.RED),Stone(11,Color.RED),testStone]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="10_11_x")

    def test_simpleStoneVariant_10_11_x_13(self):
        testStone = Stone(12,Color.RED)
        area = [Stone(10,Color.RED),Stone(11,Color.RED),testStone,Stone(13,Color.RED)]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="10_11_x_13")

    def test_simpleStoneVariant_10_11_13_x_1(self):
        testStone = Stone(1,Color.RED)
        area = [Stone(10,Color.RED),Stone(11,Color.RED),Stone(13,Color.RED),testStone]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="10_11_13_x_1")

    def test_simpleStoneVariant_x_2_3_4(self):
        testStone = Stone(1,Color.RED)
        area = [testStone,Stone(2,Color.RED),Stone(3,Color.RED),Stone(4,Color.RED)]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="x_2_3_4")

    def test_simpleStoneVariant_x_j_3_4(self):
        testStone = Stone(1,Color.RED)
        area = [testStone, Stone(0,Color.JOKER),Stone(3,Color.RED),Stone(4,Color.RED)]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="x_j_3_4")

    def test_simpleStoneVariant_1_2_j_x(self):
        testStone = Stone(4,Color.RED)
        area = [Stone(1,Color.RED),Stone(2,Color.RED),Stone(0,Color.JOKER),testStone]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="1_2_j_x")

    def test_simpleStoneVariant_10_11_j_x(self):
        testStone = Stone(12,Color.RED)
        area = [Stone(10,Color.RED),Stone(11,Color.RED),Stone(0,Color.JOKER),testStone]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="10_11_j_x")

    def test_simpleStoneVariant_8_9_j_x(self):
        testStone = Stone(11,Color.RED)
        area = [Stone(8,Color.RED),Stone(8,Color.RED),Stone(0,Color.JOKER),testStone]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="8_9_j_x")

    def test_simpleStoneVariant_8_9_x_j(self):
        testStone = Stone(10,Color.RED)
        area = [Stone(8,Color.RED),Stone(9,Color.RED),testStone,Stone(0,Color.JOKER)]

        self.assertEqual(10,calc_stone_value_in_area(testStone,area),msg="8_9_x_j")

    def test_simpleStoneVariant_7_8_x_j(self):
        testStone = Stone(9,Color.RED)
        area = [Stone(7,Color.RED),Stone(8,Color.RED),testStone,Stone(0,Color.JOKER)]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="7_8_x_j")

    def test_simpleStoneVariant_j_2_j_x(self):
        testStone = Stone(4,Color.RED)
        area = [Stone(0,Color.JOKER),Stone(2,Color.RED),Stone(0,Color.JOKER),testStone]

        self.assertEqual(5,calc_stone_value_in_area(testStone,area),msg="j_2_j_x")

    def test_simpleStoneVariant_x_1_1(self):
        testStone = Stone(1,Color.RED)
        area = [testStone,Stone(1,Color.RED),Stone(1,Color.RED)]

        self.assertEqual(25,calc_stone_value_in_area(testStone,area),msg="x_1_1")

    def test_simpleStoneVariant_1_x_1(self):
        testStone = Stone(1,Color.RED)
        area = [Stone(1,Color.RED),testStone,Stone(1,Color.RED)]

        self.assertEqual(25,calc_stone_value_in_area(testStone,area),msg="1_x_1")

    def test_simpleStoneVariant_1_1_x(self):
        testStone = Stone(1, Color.RED)
        area = [Stone(1, Color.RED), Stone(1, Color.RED),testStone]

        self.assertEqual(25, calc_stone_value_in_area(testStone, area), msg="1_1_x")

    def test_simpleStoneVariant_1_1_x_j(self):
        testStone = Stone(1, Color.RED)
        area = [Stone(1, Color.RED), Stone(1, Color.RED),testStone,Stone(0, Color.JOKER)]

        self.assertEqual(25, calc_stone_value_in_area(testStone, area), msg="1_1_x_j")

    def test_simpleStoneVariant_1_j_x_j(self):
        testStone = Stone(1, Color.RED)
        area = [Stone(1, Color.RED), Stone(0, Color.JOKER),testStone,Stone(0, Color.JOKER)]

        self.assertEqual(25, calc_stone_value_in_area(testStone, area), msg="1_j_x_j")

    def test_simpleStoneVariant_j_x_1_j(self):
        testStone = Stone(1, Color.RED)
        area = [Stone(0, Color.JOKER),testStone,Stone(1, Color.RED),Stone(0, Color.JOKER)]

        self.assertEqual(25, calc_stone_value_in_area(testStone, area), msg="j_x_1_j")



if __name__ == '__main__':
    unittest.main()