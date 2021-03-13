# -*- coding: utf-8 -*-

from py.models.reglage import Reglage

class ReglageInt(Reglage):
    def __init__(self, id, nomCourt, nomAffichage, groupe, value = 0):
        self.id = id
        self.type = "int"
        self.nomCourt = nomCourt
        self.nomAffichage = nomAffichage
        self.groupe = groupe
        self.saveValue(value)

    def valueToString(self):
        return str(self.value)

    def saveValue(self, value):
        self.value = int(value)

    def addPacket(self):
        pass

    def updatePacket(self):
        pass
