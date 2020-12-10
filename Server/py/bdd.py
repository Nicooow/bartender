# -*- coding: utf-8 -*-
import mysql.connector

class BDD():
    def __init__(self, bartender):
        self.bartender = bartender
        self.db = None

    def connect(self):
        self.bartender.log("Bdd", "Connexion à la base de donnée...")
        try:
            self.db = mysql.connector.connect(host=self.bartender.config["bdd"]["host"],
                                              user=self.bartender.config["bdd"]["user"],
                                              password=self.bartender.config["bdd"]["password"],
                                              database=self.bartender.config["bdd"]["database"])
            self.bartender.log("Bdd", "Connexion réussite")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors de la connexion : " + str(e))

    def save(self):
        pass

    def load(self):
        pass
