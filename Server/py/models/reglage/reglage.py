# -*- coding: utf-8 -*-

class Reglage():
    def __init__(self, id, nomCourt, nomAffichage, groupe, value = None):
        self.id = id
        self.type = ""
        self.nomCourt = nomCourt
        self.nomAffichage = nomAffichage
        self.groupe = groupe
        self.value = value

    def valueToString(self):
        pass

    def saveValue(self, value):
        pass

    def addPacket(self):
        pass

    def updatePacket(self):
        pass
