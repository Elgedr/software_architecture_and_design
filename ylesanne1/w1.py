import math
import typing


class Point:
    """Two-dimensional points"""

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self._x = x
        self._y = y

    def __str__(self):
        result = "\n".join(["x: %f" % self.x(),
                            "y: %f" % self.y(),
                            "rho: %f" % self.rho(),
                            "theta: %f" % self.theta()])
        return result

    # Queries

    def x(self) -> float:
        """
        Abscissa
        POST:
        Result = rho * cos(theta)
        """
        return self._x

    def y(self) -> float:
        """Ordinate"""
        return self._y

    def rho(self) -> float:
        """
        Distance to origin (0, 0)
        POST:
        Result=sqrt(x**2+y**2)
        """
        return math.sqrt(self.x() ** 2 + self.y() ** 2)

    def theta(self) -> float:
        """Angle to horizontal axis"""
        return math.atan2(self.y(), self.x())

    def distance(self, other: object) -> float:
        "Distance to other Point"
        return self.vectorTo(other).rho()

    def vectorTo(self, other: object) -> object:
        """
        Returns the Point representing the vector from self to other Point
        POST:
        Result = Point(other.x() - self.x(), other.y() - self.y())
        Result.x = ....
        Result.y = ....
        """
        return Point(other.x() - self.x(), other.y() - self.y())

    # Commands

    def translate(self, dx: float, dy: float):
        """
        Move by dx horizontally, dy vertically
        x = old x + dx
        y = old y + dy
        """
        self._x += dx
        self._y += dy

    def scale(self, factor: float):
        "Scale by factor"
        self._x *= factor
        self._y *= factor

    def centre_rotate(self, angle: float):
        """
        Rotate around origin (0, 0) by angle
        POST:
        theta = old theta + angle
        """
        temp_x = self.rho() * math.cos(self.theta() + angle)
        temp_y = self.rho() * math.sin(self.theta() + angle)
        self._x, self._y = temp_x, temp_y

    def rotate(self, p: object, angle: float):
        """
        Rotate around Point p by angle
        POST:
        p.vectorTo(self).theta() === p.vectorTo(old self).theta() + angle (NB! Nurkade võrdlus)
        """
        self.translate(-p.x(), -p.y())
        self.centre_rotate(angle)
        self.translate(p.x(), p.y())


# ylesanne 1 A
p1 = Point()
p1.translate(10, 20)
p2 = Point()
p2.translate(-20, 60)
print(p1.distance(p2))

# ylesanne 1 B
p3 = Point(15, 0)
p3.centre_rotate(math.pi / 3)  # Rotate around the origin by Pi/3

# Output polar coordinates (rho, theta) after rotation
print(f"Polar coordinates after rotation: rho = {p3.rho()}, theta = {p3.theta()}")
