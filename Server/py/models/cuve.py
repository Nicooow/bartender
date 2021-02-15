# -*- coding: utf-8 -*-

class Cuve():
    def __init__(self, id, boisson, quantite, quantiteMax, pompePinId, debitmetrePinId, debitmetreMlParTick):
        self.id = id
        self.boisson = boisson
        self.quantite = quantite
        self.quantiteMax = quantiteMax
        self.pompePinId = pompePinId
        self.debitmetrePinId = debitmetrePinId
        self.debitmetreMlParTick = debitmetreMlParTick

    def addPacket(self):
        packet = []
        packet.append("addElement")
        packet.append("cuve")
        packet.append(str(self.id))
        packet.append(str(self.quantite))
        packet.append(str(self.quantiteMax))
        packet.append(str(int( (100-(self.quantite*100/self.quantiteMax))/100*250 ))) # niveau remplis /250
        packet.append(str(self.pompePinId))
        packet.append(str(self.debitmetrePinId))
        packet.append(str(self.debitmetreMlParTick))
        if(self.boisson == None):
            packet.append("-1")
            packet.append("nomAffichage")
            packet.append("nom")
            packet.append("#fff")
        else:
            packet.append(str(self.boisson.id))
            packet.append(str(self.boisson.nomAffichage))
            packet.append(str(self.boisson.nomCourt))
            packet.append(str(self.boisson.couleur))
        return "|".join(packet)
