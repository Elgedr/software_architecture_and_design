#coding: utf-8
#coding: utf-8
import planets, math


class PSController:
    """
    Fassaadikontroller
    """

    def make_solar_system(self, T=4):
        """
        Seob kontrolleriga päikesesüsteemi mudeli.
        T määrab, mitu atomaarset tick sammu on Maa aastas
        """
        self._sys = planets.PlanetarySystem()
        # Päikesesüsteemi infol, koosneb paaridest  (aasta pikkus, kaugus päikesest)) 
        astro_data = [
            (87.97/365.26, 0.39),
            (227.7/365.26, 0.72),
            (1.0, 1.0),
            (686.98/365.26, 1.52),
            (11.86, 5.2),
            (29.46, 9.54),
            (84.01, 19.18),
            (164.81, 30.06),
            (247.7, 39.75)
            ]
        for o, r in astro_data:
            self._sys.append(planets.Planet(r, 0.0, (2 * math.pi) / (o * T)))
        
    def system(self):
        """
        Tagastab kontrolleriga seotud süsteemi
        """
        return self._sys

    def tick(self):
        """
        Muudab planeedisüsteemi elementide koordinaate atomaarse sammu võrra
        """
        self.system().tick()
        
    def multi_tick(self, N=100):
        """
        Muudab planeedisüsteemi elementide koordinaate N sammu võrra
        """
        for i in range(N):
            self.tick()

    def launch(self, planet_index, dx, dy):
        """
        Planeedi planeet_index orbiidile saadetava kosmoselaeva loomine
        """
        planet = self.system()[planet_index]
        ship = planets.SpaceShip(planet.x(), planet.y(), dx, dy)
        self._sys.append(ship)
        return ship
