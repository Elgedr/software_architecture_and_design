import unittest
import math


class TestRadians(unittest.TestCase):

    def assertRadiansEqual(self, expected, actual, places=7, msg=""):
        rem = (expected - actual) % (2 * math.pi)  # Finds the remainder
        diff = min(rem, 2 * math.pi - rem)  # Remainder can be just short of 2pi, take the smaller angle
        return self.assertAlmostEqual(0.0, diff, places, msg)

    def testRadianEquality(self):
        self.assertRadiansEqual(1.0, 1.0, msg="Simple equality failure")
        self.assertRadiansEqual((3 / 2) * math.pi, -(1 / 2) * math.pi, msg="Negative radian equality failure")
        self.assertRadiansEqual((3 / 2) * math.pi, (7 / 2) * math.pi, msg="Modulo radian equality failure")
        self.assertRadiansEqual((3 / 2) * math.pi, -(5 / 2) * math.pi, msg="Negative modulo radian equality failure")


if __name__ == '__main__':
    unittest.main()