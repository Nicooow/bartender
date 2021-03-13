# -*- coding: utf-8 -*-

class Reglages():
    def __init__(self, id, nomCourt, nomAffichage):
        self.id = id
        self.nomCourt = nomCourt
        self.nomAffichage = nomAffichage
        self.reglages = {}

    def addPacket(self):
        pass

    def addReglage(self, reglage):
        self.reglages[reglage.id] = reglage;
