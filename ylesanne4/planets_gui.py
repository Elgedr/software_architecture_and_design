#coding: utf-8
"""
Planeedisüsteemi simulatsiooni graafiline kasutajaliides.
Kasutab Pythoni standard kasutajaliidese-raamistikku Tkinter.

Käivitamiseks kirjutada Command Prompti:
    pythonw planets_ui.py
"""
try:
    from Tkinter import *
except:
    from tkinter import *

import planets_facade

class Application(Frame):
    """Ühest aknast koosnev lihtne kasutajaliides"""

    def __init__(self, master=None):
        "Initsialiseerimine"
        Frame.__init__(self, master)
        self.controller = planets_facade.PSController()
        self.po_dict = {}
        self.planet_width = 3
        self.zoom = 6
        self.auto_speed = 100
        self.auto_on = 0
        self.cx, self.cy = 300, 300
        self.pack()
        self.createWidgets()
        self.make_solar_system()

    def tick(self):
        """
        (Kasutaja on vajutanud Tick-nuppu.) 
        Saada sõnum kontrollerile ja kuva planeedid uutel asukohtadel.
        """
        self.controller.tick()
        self.move_planets()

    def launch(self):
        ship = self.controller.launch(3, 0.5, 0.5)
        id = len(self.controller.system()) - 1
        self.draw_planet(id, ship.x(), ship.y())

    def tick100(self):
        """
        (Kasutaja on vajutanud Tick100-nuppu.) 
        Saada sõnum kontrollerile ja kuva planeedid uutel asukohtadel.
        """
        self.controller.multi_tick(100)
        self.move_planets()

    def auto(self):
        self.auto_on = not self.auto_on
        self.autoTick()

    def autoTick(self):
        if self.auto_on:
            self.tick()
            self.after(self.auto_speed, self.autoTick)

    def make_solar_system(self):
        "Planeedisüsteemi initsialiseerimine"
        self.controller.make_solar_system()
        self.delete_planets()
        self.draw_planets()

    def createWidgets(self):
        "Erinevate kasutajaliidese vidinate tekitamine"
        self.canv = Canvas(self, background = 'black', width = self.cx * 2, height=self.cy * 2)
        self.canv.pack({"side": "left"})
        self.canv.create_oval(self.cx, self.cy, self.cx + self.planet_width, 
            self.cy + self.planet_width, fill = "yellow")
        self.bTick = Button(self, text="Tick", command=self.tick)
        self.bTick.pack()
        self.bTick100 = Button(self, text="Tick 100", command=self.tick100)
        self.bTick100.pack()
        self.bAuto = Button(self, text="Auto", command=self.auto)
        self.bAuto.pack()
        self.bDefault = Button(self, text="Solar system", command=self.make_solar_system)
        self.bDefault.pack()
        self.bLaunch = Button(self, text="Launch", command=self.launch)
        self.bLaunch.pack()

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
        x1 = x0 + self.planet_width
        y1 = y0 + self.planet_width
        return x0, y0, x1, y1
    
    def draw_planets(self):
        """
        Joonistab ekraanile esimest korda olemasolevad planeedid,
        konverteerides koordinaadid sobivale kujule
        """
        sys = self.controller.system()
        for id in range(len(sys)):
            self.draw_planet(id, sys[id].x(), sys[id].y())
    
    def draw_planet(self, planet_id, x, y):
        """
        Joonistab esimest korda x, y koordinaatidega planeedi, 
        konverteerides koordinaadid sobivale kujule
        """
        x0, y0, x1, y1 = self.conv_coords(x, y)
        oval_id = self.canv.create_oval(x0, y0, x1, y1, fill = "white")
        self.po_dict[planet_id] = oval_id
    
    def move_planets(self):
        """
        Liigutab ekraanil kõiki olemasolevaid planeete
        """
        sys = self.controller.system()
        for id in range(len(sys)):
            self.move_planet(id, sys[id].x(), sys[id].y())
    
    def move_planet(self, planet_id, x, y): 
        """
        Liigutab ekraanil juba olemasolevat planeeti
        """
        x0, y0, x1, y1 = self.conv_coords(x, y)
        self.canv.coords(self.po_dict[planet_id], x0, y0, x1, y1)
        
    def delete_planets(self):
        " Kustutab kõik kuvatud planeedid"
        for id in self.po_dict.values():
            self.canv.delete(id)
        self.po_dict = {}
        


# Põhiprogramm
app = Application()
app.mainloop()
