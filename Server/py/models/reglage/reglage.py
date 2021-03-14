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
        return str(value)

    def saveValue(self, value):
        pass

    def addPacket(self):
        packet = []
        packet.append("addElement")
        packet.append("reglage")
        packet.append(str(self.id))
        packet.append(str(self.type))
        packet.append(str(self.nomCourt))
        packet.append(str(self.nomAffichage))
        packet.append(self.valueToString())
        return "|".join(packet)

    def updatePacket(self):
        pass
