# -*- coding: utf-8 -*-

from py.models.reglage.reglage import Reglage

class ReglageInt(Reglage):
    def __init__(self, id, nomCourt, nomAffichage, groupe, value = 0):
        self.id = id
        self.type = "int"
        self.nomCourt = nomCourt
        self.nomAffichage = nomAffichage
        self.groupe = groupe

        self.eventHandler = lambda *args: None
        self.saveValue(value)


    def valueToString(self):
        return str(self.value)

    def saveValue(self, value):
        self.value = int(value)
        super(ReglageInt, self).onValueChange(value, self.value)
