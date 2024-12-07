# Oleku abstraktne klass
class PoordvaravaOlek:
    def münt(self, poordvarav):
        pass

    def möödu(self, poordvarav):
        pass


# Suletud olek
class SuletudOlek(PoordvaravaOlek):
    def münt(self, poordvarav):
        print("Ava: Pöördvärav avati.")
        poordvarav.määra_avatuks()

    def möödu(self, poordvarav):
        print("Alarm: Möödumine keelatud!")


# Avatud olek
class AvatudOlek(PoordvaravaOlek):
    def münt(self, poordvarav):
        print("Täna: Münt juba lisatud.")

    def möödu(self, poordvarav):
        print("Sule: Pöördvärav suleti.")
        poordvarav.määra_suletuks()


# Pöördvärava klass
class Poordvarav:
    def __init__(self):
        self.olek = SuletudOlek()  # Algolek

    def määra_avatuks(self):
        self.olek = AvatudOlek()

    def määra_suletuks(self):
        self.olek = SuletudOlek()

    def münt(self):
        self.olek.münt(self)

    def möödu(self):
        self.olek.möödu(self)


# Testimine
if __name__ == "__main__":
    pv = Poordvarav()

    # Sündmuste järjestus
    pv.münt()  # Ava
    pv.münt()  # Täna
    pv.möödu()  # Sule
    pv.möödu()  # Alarm
