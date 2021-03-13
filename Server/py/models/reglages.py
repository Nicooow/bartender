# -*- coding: utf-8 -*-

class Reglages():
    def __init__(self, id, nomCourt, nomAffichage):
        self.id = id
        self.nomCourt = nomCourt
        self.nomAffichage = nomAffichage
        self.reglage = []

    def addPacket(self):
        pass

    def addReglage(self, reglage):
        self.reglage.append(reglage);
