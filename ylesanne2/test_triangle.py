import unittest
import math
from triangle import Triangle


class TestTriangle(unittest.TestCase):

    def setUp(self):
        self.triangle = Triangle(2, 3, 4)

    def testInvariants(self):
        self.assertAlmostEqual(math.pi, self.triangle.alfa() + self.triangle.beta() + self.triangle.gamma())
        self.assertAlmostEqual(self.triangle.a / math.sin(self.triangle.alfa()),
                               self.triangle.b / math.sin(self.triangle.beta()))
        self.assertAlmostEqual(self.triangle.c / math.sin(self.triangle.gamma()),
                               self.triangle.b / math.sin(self.triangle.beta()))

    def testCircumference(self):
        self.assertAlmostEqual(9, self.triangle.circumference())

    def testScale(self):
        self.triangle.scale(10)
        self.assertAlmostEqual(20, self.triangle.a)
        self.assertAlmostEqual(30, self.triangle.b)
        self.assertAlmostEqual(40, self.triangle.c)
        self.testInvariants()


if __name__ == "__main__":
    unittest.main()
