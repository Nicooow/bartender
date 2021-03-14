# -*- coding: utf-8 -*-

class Reglages():
    def __init__(self, id, nomCourt, nomAffichage):
        self.id = id
        self.nomCourt = nomCourt
        self.nomAffichage = nomAffichage
        self.reglages = {}

    def addPacket(self):
        packet = []
        packet.append("addElement")
        packet.append("reglages")
        packet.append(str(self.id))
        packet.append(str(self.nomCourt))
        packet.append(str(self.nomAffichage))
        return "|".join(packet)

    def addReglage(self, reglage):
        self.reglages[reglage.id] = reglage;
