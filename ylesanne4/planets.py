# coding: utf-8
import geom


class Planet(geom.Point):
    "Planeet omab koordinaate ja nurkkiirust. Tiirleb ümber koordinaatide alguspunkti."

    def __init__(self, x, y, omega):
        geom.Point.__init__(self, x, y)
        self._omega = omega

    def omega(self):
        "Nurkkiirus radiaanides"
        return self._omega

    def tick(self):
        """
        Atomaarne samm planeedi simulatsioonis.
        Planeedi koordinaadid muutuvad nurkkiiruse võrra
        """
        self.centre_rotate(self.omega())


class PlanetarySystem(list):
    "Planeetide hulk (list)"

    def tick(self):
        """
        Atomaarne samm planeedisüsteemi simulatsioonis.
        Kõigi planeedisüsteemi elementide tick opertsiooni sooritamine
        """
        for item in self:
            item.tick()

    def distance(self, i1, i2):
        """
        Kaugus indekseid i1 ja i2 omavate süsteemi elementide vahel
        """
        return self[i1].distance(self[i2])

    def __str__(self):
        "Planeedisüsteemi kirjeldav string (print ja str operatsioonid)"
        return '\n---\n'.join([str(p) for p in self])


"""Spaceship class"""
from geom import Point


class SpaceShip(Point):
    """Spaceship class"""

    def __init__(self, x: int, y: int, dx: float, dy: float):
        Point.__init__(self, x, y)
        self._dx = dx
        self._dy = dy

    def dx(self):
        return self._dx

    def dy(self):
        return self._dy

    def tick(self):
        self._x += self._dx
        self._y += self._dy


if __name__ == "__main__":
    ps = PlanetarySystem()
    ps.append(Planet(5, 0, 0.1))
    ps.append(Planet(10, 0, 0.1))
    ps.append(Planet(15, 0, 0.2))
    for i in range(10):
        ps.tick()
