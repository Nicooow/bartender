# -*- coding: utf-8 -*-

class Cuve():
    def __init__(self, id, boisson, quantitee, quantiteeMax, pompePinId, debitmetrePinId, debitmetreMlParTick):
        self.id = id
        self.boisson = boisson
        self.quantitee = quantitee
        self.quantiteeMax = quantiteeMax
        self.pompePinId = pompePinId
        self.debitmetrePinId = debitmetrePinId
        self.debitmetreMlParTick = debitmetreMlParTick

    def addPacket(self):
        pass
        """
        packet = []
        packet.append("addElement")
        packet.append("boisson")
        packet.append(str(self.id))
        packet.append(str(self.nomAffichage))
        packet.append(str(self.nomCourt))
        packet.append(str(self.couleur))
        packet.append(str(self.pourcentageAlcool))
        packet.append(str(int(self.editing)))
        packet.append(str(self.logo))
        return "|".join(packet)
        """
