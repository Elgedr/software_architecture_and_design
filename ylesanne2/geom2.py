import math


class Point:
    "Two-dimensional points"

    def __init__(self, x: float = 0.0, y: float = 0.0):
        """
        PRE: -
        POST:
        self.x == x
        self.y == y
        """
        self._rho = math.sqrt(x ** 2 + y ** 2)
        self._theta = math.atan2(y, x)

    def __str__(self) -> str:
        result = "\n".join(["x: %f" % self.x(),
                            "y: %f" % self.y(),
                            "rho: %f" % self.rho(),
                            "theta: %f" % self.theta()])
        return result

    # Queries

    def x(self) -> float:
        """
        Abscissa
        PRE:
        POST:
        Result = self.rho()* math.cos(self.theta())
        """
        return self.rho() * math.cos(self.theta())

    def y(self) -> float:
        "Ordinate"
        return self.rho() * math.sin(self.theta())

    def rho(self) -> float:
        """
        Distance to origin (0, 0)
        pre:-
        post: Result = sqrt(x**2+y**2)
        """
        return self._rho

    def theta(self) -> float:
        "Angle to horizontal axis"
        return self._theta

    def distance(self, other: object) -> float:
        "Distance to other"
        return self.vectorTo(other).rho()

    def vectorTo(self, other: object) -> object:
        "Returns the Point representing the vector from self to other Point"
        return Point(other.x() - self.x(), other.y() - self.y())

    # Commands

    def translate(self, dx: float, dy: float):
        """
        Move by dx horizontally, dy vertically
        PRE: -
        POST:
        x == old x + dx
        y == old y + dy
        """
        x = self.x() + dx
        y = self.y() + dy
        self._rho = math.sqrt(x ** 2 + y ** 2)
        self._theta = math.atan2(y, x)

    def scale(self, factor: float):
        "Scale by factor"
        if factor < 0:
            self.centre_rotate(math.pi)
            self._rho *= -factor
        else:
            self._rho *= factor

    def centre_rotate(self, angle: float):
        """
        Rotate around origin (0, 0) by angle
        PRE:-
        POST: theta() == old theta() + angle  (NB! Nurkade võrdlus)
        """
        self._theta = (self._theta + angle) % (2 * math.pi)

    def rotate(self, p: object, angle: float):
        """
        Rotate around p by angle
        PRE: -
        POST:
        p.vectorTo(self).theta() == p.vectorTo(old self).theta() + angle (NB! Nurkade võrdlus)
        """
        self.translate(-p.x(), -p.y())
        self.centre_rotate(angle)
        self.translate(p.x(), p.y())
