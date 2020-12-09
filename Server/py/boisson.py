# -*- coding: utf-8 -*-

class Boisson():
    def __init__(self, bartender):
        self.bartender = bartender
        self.bartender.log("boisson", "Creation d'une boisson")

        self.id = 0
        self.nomAffichage = ""
        self.nomCourt = ""
        self.couleur = "#ffffff"
        self.pourcentageAlcool = 0
