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
        packet = []
        packet.append("addElement")
        packet.append("cuve")
        packet.append(str(self.id))
        packet.append(str(self.quantitee))
        packet.append(str(self.quantiteeMax))
        packet.append(str(int( (100-(self.quantitee*100/self.quantiteeMax))/100*250 ))) # pourcentage remplis
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
