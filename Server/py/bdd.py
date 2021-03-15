# -*- coding: utf-8 -*-
import mysql.connector
from py.models.boisson import Boisson
from py.models.cuve import Cuve
from py.models.reglages import Reglages
from py.models.reglage.reglage import Reglage
from py.models.reglage.reglageInt import ReglageInt
from py.models.reglage.reglageColor import ReglageColor

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

    def disconnect(self):
        self.bartender.log("Bdd", "Déconnexion de la base de donnée...")
        try:
            self.db.close()
            self.bartender.log("Bdd", "Déconnecté")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors de la déconnexion : " + str(e))
            self.db = None

    def load(self):
        self.bartender.log("Bdd", "Chargement des données...")
        if(self.db == None):
            self.bartender.log("Bdd", "Base de donnée non connectée, abandon")
            return

        boissons = {}
        cuves = {}
        reglages = {}

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
            self.cursor.execute("SELECT * FROM cuve")
            for c in self.cursor:
                bCuve = boissons[c[1]] if (c[1] in boissons) else None
                cuve = Cuve(c[0], bCuve, c[2], c[3], c[4], c[5], c[6], c[7])
                cuves[c[0]] = cuve
            self.bartender.log("Bdd", f"{len(cuves)} cuves chargés")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors du chargement des cuves")
            print(e)

        try:
            self.cursor.execute("SELECT * FROM reglages")
            for r in self.cursor:
                reg = Reglages(r[0], r[1], r[2])
                reglages[r[0]] = reg
            self.bartender.log("Bdd", f"{len(reglages)} groupe de réglages chargés")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors du chargement des groupes de réglages")
            print(e)

        try:
            self.cursor.execute("SELECT * FROM reglage")
            i = 0
            for r in self.cursor:
                i+=1
                typeString = {"int": ReglageInt, "color": ReglageColor}
                if(r[1] in typeString):
                    typeObject = typeString[r[1]]
                    reg = typeObject(r[0], r[2], r[3],  reglages[r[5]], r[4])
                else:
                    reg = Reglage(r[0], r[2], r[3],  reglages[r[5]], r[4], r[1])
                reglages[r[5]].addReglage(reg)
            self.bartender.log("Bdd", f"{i} réglages chargés")
        except Exception as e:
            self.bartender.log("Bdd", "Erreur lors du chargement des réglages")
            print(e)

        self.bartender.boissons = boissons
        self.bartender.cuves = cuves
        self.bartender.reglages = reglages

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

    def updateBoisson(self, idToUpdate, nomAffichage, nomCourt, couleur, pourcentageAlcool, logo):
        if(not int(idToUpdate) in self.bartender.boissons):
            raise Exception("Boisson inexistante. Cette erreur n'est pas censée arriver.")

        boisson = self.bartender.boissons[int(idToUpdate)]

        if(logo == ""):
            logo = boisson.logo

        sql = ("UPDATE boisson SET nomAffichage = %s, nomCourt = %s, couleur = %s, pourcentageAlcool = %s, logo = %s WHERE id = %s")
        self.cursor.execute(sql, (nomAffichage, nomCourt, couleur, pourcentageAlcool, logo, idToUpdate))
        boisson.nomAffichage = nomAffichage
        boisson.nomCourt = nomCourt
        boisson.couleur = couleur
        boisson.pourcentageAlcool = pourcentageAlcool
        boisson.logo = logo
        self.db.commit()
        self.bartender.log("Bdd", f"Boisson modifiée (id:{self.cursor.lastrowid})")
        return boisson

    def deleteBoisson(self, idToDelete):
        if(not int(idToDelete) in self.bartender.boissons):
            raise Exception("Boisson inexistante. Cette erreur n'est pas censée arriver.")

        sql = ("DELETE FROM boisson WHERE id = %s")
        self.cursor.execute(sql, (idToDelete,))
        self.db.commit()
        del self.bartender.boissons[int(idToDelete)]

        self.bartender.log("Bdd", f"Boisson supprimée (id:{self.cursor.lastrowid})")

    def newCuve(self, quantite, quantiteMax, pompePinId, dmPinId, dmMlParTick, bId):
        if(not int(bId) in self.bartender.boissons):
            if(int(bId) == -1):
                boisson = None
            else:
                raise Exception("Boisson contenue inexistante. Cette erreur n'est pas censée arriver.")
        else:
            boisson = self.bartender.boissons[int(bId)]

        sql = ("INSERT INTO cuve "
                      "(idBoisson, quantite, quantiteMax, pompePinId, debitmetrePinId, debitmetreMlParTick)"
                      "VALUES (%s, %s, %s, %s, %s, %s)")
        self.cursor.execute(sql, (bId, quantite, quantiteMax, pompePinId, dmPinId, dmMlParTick))
        self.bartender.cuves[self.cursor.lastrowid] = Cuve(self.cursor.lastrowid, boisson, quantite, quantiteMax, pompePinId, dmPinId, dmMlParTick, True)
        self.db.commit()
        self.bartender.log("Bdd", f"Cuve créée (id:{self.cursor.lastrowid})")
        return self.bartender.cuves[self.cursor.lastrowid]

    def updateCuve(self, idToUpdate, quantite, quantiteMax, pompePinId, dmPinId, dmMlParTick, bId, enabled):
        if(not int(bId) in self.bartender.boissons):
            if(int(bId) == -1):
                boisson = None
            else:
                raise Exception("Boisson contenue inexistante. Cette erreur n'est pas censée arriver.")
        else:
            boisson = self.bartender.boissons[int(bId)]

        if(not int(idToUpdate) in self.bartender.cuves):
            raise Exception("Cuve inexistante. Cette erreur n'est pas censée arriver.")

        cuve = self.bartender.cuves[int(idToUpdate)]

        sql = ("UPDATE cuve SET idBoisson = %s, quantite = %s, quantiteMax = %s, pompePinId = %s, debitmetrePinId = %s, debitmetreMlParTick = %s, enabled=%s WHERE id = %s")
        self.cursor.execute(sql, (bId, quantite, quantiteMax, pompePinId, dmPinId, dmMlParTick, enabled, idToUpdate))
        cuve.boisson = boisson
        cuve.quantite = quantite
        cuve.quantiteMax = quantiteMax
        cuve.pompePinId = pompePinId
        cuve.debitmetrePinId = dmPinId
        cuve.debitmetreMlParTick = dmMlParTick
        cuve.enabled = enabled
        self.db.commit()
        self.bartender.log("Bdd", f"Cuve modifiée (id:{self.cursor.lastrowid})")
        return cuve

    def deleteCuve(self, idToDelete):
        if(not int(idToDelete) in self.bartender.cuves):
            raise Exception("Cuve inexistante. Cette erreur n'est pas censée arriver.")

        sql = ("DELETE FROM cuve WHERE id = %s")
        self.cursor.execute(sql, (idToDelete,))
        self.db.commit()
        del self.bartender.cuves[int(idToDelete)]

        self.bartender.log("Bdd", f"Cuve supprimée (id:{self.cursor.lastrowid})")

    def updateReglage(self, reglage, newValue):
        reglage.saveValue(newValue)

        sql = ("UPDATE reglage SET valeur = %s WHERE id = %s")
        self.cursor.execute(sql, (reglage.valueToString(), reglage.id))

        self.db.commit()
