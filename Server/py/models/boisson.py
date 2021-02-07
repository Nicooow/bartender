# -*- coding: utf-8 -*-

class Boisson():
    def __init__(self, id, nomAffichage, nomCourt, couleur, pourcentageAlcool, logo):
        self.id = id
        self.nomAffichage = nomAffichage
        self.nomCourt = nomCourt
        self.couleur = couleur
        self.pourcentageAlcool = pourcentageAlcool
        self.logo = logo
        self.editing = False

    def addPacket(self):
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

    def updatePacket(self):
        packet = []
        packet.append("updateElement")
        packet.append(str(self.id))
        packet.append("boisson")
        packet.append(str(self.nomAffichage))
        packet.append(str(self.nomCourt))
        packet.append(str(self.couleur))
        packet.append(str(self.pourcentageAlcool))
        packet.append(str(self.logo))
        return "|".join(packet)
