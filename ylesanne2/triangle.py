import math


class Triangle:
    """
    INV:
    self.alfa()+self.beta()+self.gamma() == math.pi
    self.a/math.sin(self.alfa()) == self.b/math.sin(self.beta()) == self.c/math.sin(self.gamma())
    """

    def __init__(self, a, b, c):
        """
        PRE:
        a>0
        b>0
        c>0

        POST:
        self.a==a
        self.b==b
        self.c==c
        """
        self.a = a
        self.b = b
        self.c = c

    def alfa(self): return self.angle_from_sides(self.b, self.c, self.a)

    def beta(self): return self.angle_from_sides(self.a, self.c, self.b)

    def gamma(self): return self.angle_from_sides(self.b, self.a, self.c)

    def angle_from_sides(self, a, b, c):
        """
        a, b are left and right sides from angle, c is opposite side
        """
        return math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

    def circumference(self):
        """
        PRE:-
        POST: Result == (self.a + self.b + self.c)
        """
        return self.a + self.b + self.c

    def scale(self, k):
        """
        PRE: k>0
        POST:
        self.a == old self.a*k
        self.b == old self.b*k
        self.c == old self.c*k
        """
        self.a = self.a * k
        self.b = self.b * k
        self.c = self.c * k




