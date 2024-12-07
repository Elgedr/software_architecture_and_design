class Tarkvara:
    """
    Klass erinevate OS-ide installeerijate jaoks
    """

    def __init__(self, baaskataloog, os_strat):
        self.baaskataloog = baaskataloog
        self.os = os_strat

    def installeeri(self):
        """
        Meetod, mis installeerib tarkvara
        """
        if not self.os.kataloog_sobib(self.baaskataloog):
            self.baaskataloog = "varukataloog"
        self.os.valmista_kataloog(self.baaskataloog + "\\bin")
        self.os.installeeri_failid(self.baaskataloog + "\\bin", ["proge.exe", "proge.bat"])
        self.os.valmista_kataloog(self.baaskataloog + "\\dat")
        self.os.installeeri_failid(self.baaskataloog + "\\dat", ["mudelid.dat", "andmed.dat"])


class OS:
    """
    OS liidese kirjeldus
    """

    def kataloog_sobib(self, kataloog):
        """Operatsioon, mis kontrollib, kas kataloog sobib"""
        raise NotImplementedError

    def valmista_kataloog(self, kataloog):
        """Operatsioon, mis valmistab kataloogi"""
        raise NotImplementedError

    def installeeri_failid(self, kataloog, failid):
        """Operatsioon, mis installeerib failid kataloogi"""
        raise NotImplementedError


class Windows(OS):
    """
    OS liides Windowsile
    """

    def kataloog_sobib(self, kataloog):
        print("Kontrollin kataloogi " + kataloog + " sobivust Windowsile")
        return len(kataloog) < 8

    def valmista_kataloog(self, kataloog):
        print("Valmistan kataloogi " + kataloog + " Windowsile")

    def installeeri_failid(self, kataloog, failid):
        for fail in failid:
            print("Tekitan Windowsis faili " + kataloog + "\\" + fail)


class Unix(OS):
    """
    OS liides Unixile
    """

    def kataloog_sobib(self, kataloog):
        print("Kontrollin kataloogi " + kataloog + " sobivust Unixile")
        return len(kataloog) > 2

    def valmista_kataloog(self, kataloog):
        print("Valmistan kataloogi " + kataloog + " Unixile")

    def installeeri_failid(self, kataloog, failid):
        for fail in failid:
            print("Tekitan Unixis faili " + kataloog + "\\" + fail)


class ProTarkvara(Tarkvara):
    """
    Ka tarkvara abstraktsioon võib varieeruda. Tekib silla (Bridge) muster.
    """

    def installeeri(self):
        super().installeeri()
        print("Paigaldame profilaiendused")
        self.os.valmista_kataloog(self.baaskataloog + "\\ext")
        self.os.installeeri_failid(self.baaskataloog + "\\ext", ["laiendus1.egg", "laiendus2.egg"])


def demonstreeri():
    print("Demonstreerime Windowsi Tarkvara")
    tw = Tarkvara("usr\\kataloog", Windows())
    tw.installeeri()
    print("\nDemonstreerime Unixi Tarkvara")
    tu = ProTarkvara("usr\\kataloog", Unix())
    tu.installeeri()


if __name__ == "__main__":
    demonstreeri()