from tkinter import *

from lisa5en.geom import Point
from lisa5en.sierpinski_triangle import SierpinskiTriangle
from lisa5en.planets import PlanetarySystem


class PointDrawer(Frame):
    """Ühest aknast koosnev lihtne kasutajaliides"""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.point_width = 1
        self.zoom = 1
        self.cx = 450
        self.cy = 450
        self.pack()
        self.canv = Canvas(self, background='black', width=self.cx * 2, height=self.cy * 2)
        self.canv.pack()

    def conv_coords(self, x, y):
        """
        Simulatsiooni koordinaatide konverteerimine kasutajaliidese jaoks sobivale kujule.
        Sõltub atribuutidest:
        cx, cy - kuva keskpunkt
        zoom - suurendus
        planet_width - planeedi suurus
        Väljastab ovaali joonistamiseks vajalikud neli koordinaati
        """
        x0 = self.cx + x * self.zoom
        y0 = self.cy + y * self.zoom
        x1 = x0 + self.point_width
        y1 = y0 + self.point_width
        return x0, y0, x1, y1

    def draw_triangle(self, points_iterable):
        for point in points_iterable:
            x = int(point.x())
            y = int(point.y())
            x0, y0, x1, y1 = self.conv_coords(x, y)
            self.canv.create_oval(x0, y0, x1, y1, fill="white")


if __name__ == '__main__':
    app1 = PointDrawer()
    app1.draw_triangle(PlanetarySystem())
    # app1.draw_triangle(SierpinskiTriangle(Point(0, 0), 400))
    app1.mainloop()
