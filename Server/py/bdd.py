# -*- coding: utf-8 -*-
import mysql.connector
from py.models.boisson import Boisson
from py.models.pompe import Pompe
from py.models.cuve import Cuve
from py.models.debitmetre import Debitmetre

class BDD():
    def __init__(self, bartender):
        self.bartender = bartender
        self.db = None
        self.cursor = None

    def connect(self):
        self.bartender.log("Bdd", "Connexion à la base de donnée...")
        try:
            self.db = mysql.connector.connect(host=self.bartender.config["bdd"]["host"],
                                              user=self.bartender.config["bdd"]["user"],
                                              password=self.bartender.config["bdd"]["password"],
                                              database=self.bartender.config["bdd"]["database"])
            self.cursor = self.db.cursor()
            self.bartender.log("Bdd", "Connexion réussite")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors de la connexion : " + str(e))
            self.db = None


    def load(self):
        self.bartender.log("Bdd", "Chargement des données...")
        if(self.db == None):
            self.bartender.log("Bdd", "Base de donnée non connectée, abandon")
            return

        boissons = {}
        pompes = {}
        debitmetres = {}
        cuves = {}

        try:
            self.cursor.execute("SELECT * FROM boisson")
            for b in self.cursor:
                boisson = Boisson(b[0], b[1], b[2], b[3], b[4], b[5])
                boissons[b[0]] = boisson
            self.bartender.log("Bdd", f"{len(boissons)} boissons chargés")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors du chargement des boissons")
            print(e)

        try:
            self.cursor.execute("SELECT * FROM pompe")
            for p in self.cursor:
                pompe = Pompe(p[0], p[1])
                pompes[p[0]] = pompe
            self.bartender.log("Bdd", f"{len(pompes)} pompes chargés")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors du chargement des pompes")
            print(e)

        try:
            self.cursor.execute("SELECT * FROM debitmetre")
            for d in self.cursor:
                debitmetre = Debitmetre(d[0], d[1], d[2])
                debitmetres[d[0]] = debitmetre
            self.bartender.log("Bdd", f"{len(debitmetres)} débitmètres chargés")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors du chargement des débitmètres")
            print(e)

        try:
            self.cursor.execute("SELECT * FROM cuve")
            for c in self.cursor:
                pCuve = pompes[c[1]] if (c[1] in pompes) else None
                dmCuve = debitmetres[c[2]] if (c[2] in debitmetres) else None
                bCuve = boissons[c[3]] if (c[3] in boissons) else None
                cuve = Cuve(c[0], pCuve, dmCuve, bCuve, c[4], c[5])
                cuves[c[0]] = cuve
            self.bartender.log("Bdd", f"{len(cuves)} cuves chargés")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors du chargement des cuves")
            print(e)

        self.bartender.boissons = boissons
        self.bartender.pompes = pompes
        self.bartender.debitmetres = debitmetres
        self.bartender.cuves = cuves

    def save(self):
        pass

    def newBoisson(self, nomAffichage, nomCourt, couleur, pourcentageAlcool, logo):
        sql = ("INSERT INTO boisson "
                      "(nomAffichage, nomCourt, couleur, pourcentageAlcool, logo)"
                      "VALUES (%s, %s, %s, %s, %s)")
        self.cursor.execute(sql, (nomAffichage, nomCourt, couleur, pourcentageAlcool, logo))
        self.bartender.boissons[self.cursor.lastrowid] = Boisson(self.cursor.lastrowid, nomAffichage, nomCourt, couleur, pourcentageAlcool, logo)
        self.db.commit()
        self.bartender.log("Bdd", f"Boisson créée (id:{self.cursor.lastrowid})")
        return self.bartender.boissons[self.cursor.lastrowid]
