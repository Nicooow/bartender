# -*- coding: utf-8 -*-

from py.models.reglage.reglage import Reglage

class ReglageColor(Reglage):
    def __init__(self, id, nomCourt, nomAffichage, groupe, value = "#123456"):
        self.id = id
        self.type = "color"
        self.nomCourt = nomCourt
        self.nomAffichage = nomAffichage
        self.groupe = groupe
        self.saveValue(value)

    def valueToString(self):
        return str(self.value)

    def saveValue(self, value):
        self.value = "#" + str(value).replace("#","")

    def updatePacket(self):
        pass
