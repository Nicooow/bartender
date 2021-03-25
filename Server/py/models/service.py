# -*- coding: utf-8 -*-

class Service():
    def __init__(self, boisson, cuve, quantiteService):
        self.boisson = boisson
        self.cuve = cuve
        self.quantiteService = quantiteService
        self.quantiteRestant = quantiteService
        self.terminated = False
