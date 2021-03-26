# -*- coding: utf-8 -*-

class Cuve():
    def __init__(self, id, boisson, quantite, quantiteMax, pompePinId, debitmetrePinId, debitmetreMlParTick, enabled):
        self.id = id
        self.boisson = boisson
        self.quantite = quantite
        self.quantiteMax = quantiteMax
        self.pompePinId = pompePinId
        self.debitmetrePinId = debitmetrePinId
        self.debitmetreMlParTick = debitmetreMlParTick
        self.editing = False
        self.enabled = enabled
        self.running = False

    def addPacket(self):
        self.quantite = round(float(self.quantite), 2)
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
            packet.append("???")
            packet.append("?")
            packet.append("#fff")
        else:
            packet.append(str(self.boisson.id))
            packet.append(str(self.boisson.nomAffichage))
            packet.append(str(self.boisson.nomCourt))
            packet.append(str(self.boisson.couleur))
        packet.append(str(int(self.editing)))
        packet.append(str(int(self.enabled)))
        packet.append(str(int(self.running)))
        return "|".join(packet)

    def updatePacket(self):
        self.quantite = round(float(self.quantite), 2)
        packet = []
        packet.append("updateElement")
        packet.append(str(self.id))
        packet.append("cuve")
        packet.append(str(self.quantite))
        packet.append(str(self.quantiteMax))
        packet.append(str(int( (100-(self.quantite*100/self.quantiteMax))/100*250 ))) # niveau remplis /250
        packet.append(str(self.pompePinId))
        packet.append(str(self.debitmetrePinId))
        packet.append(str(self.debitmetreMlParTick))
        if(self.boisson == None):
            packet.append("-1")
            packet.append("???")
            packet.append("?")
            packet.append("#fff")
        else:
            packet.append(str(self.boisson.id))
            packet.append(str(self.boisson.nomAffichage))
            packet.append(str(self.boisson.nomCourt))
            packet.append(str(self.boisson.couleur))
        packet.append(str(int(self.running)))
        return "|".join(packet)
