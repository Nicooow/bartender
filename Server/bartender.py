# -*- coding: utf-8 -*-

import sys
import json
import time
import traceback
import os
from py import parser, serverWs, gpioHandler, bdd, errors
from py.bcolors import bcolors
from py.models.service import Service
from py.models.reglage.reglage import Reglage

application_path = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

class Bartender():
    def __init__(self, debug=True):
        start = time.time()
        # PARAM
        self.debug = debug

        # MODULES
        self.bdd = bdd.BDD(self)
        self.parser = parser.Parser(self)
        self.ws = serverWs.ServerWs(self)
        self.gpio = gpioHandler.GPIOHandler(self)

        # DONNEES
        self.boissons = {}
        self.cuves = {}
        self.config = {}
        self.distributeur = None
        self.services = []
        self.reglages = {}

        # INIT
        self.log('__init__', "Initialisation...")
        self.loadConfig()
        self.bdd.connect()
        self.bdd.load()
        self.ws.daemon = True
        self.ws.start()
        self.gpio.load()

        # DONNEES
        self.reglageThemeCouleur = self.getReglage("THEME", "COLOR", "#ff0000")
        self.reglageThemeCouleur.eventHandler = self.onThemeCouleurChange

        self.log("__init__", f"Initialisation terminée en {round(time.time()-start,3)} secondes.")

    def exit(self):
        self.bdd.disconnect()
        self.ws.close()
        self.gpio.stop()

    def log(self, func, text):
        color = ["", ""]
        maxLength = 100
        text = text[:maxLength] + ("..." if len(text) > maxLength else "")
        colorFunc = {'ServerWs': [bcolors.CYELLOW, bcolors.CYELLOW2],
                     'Parser': [bcolors.CVIOLET, bcolors.CVIOLET2],
                     'Bdd': [bcolors.CBLUE, bcolors.CBLUE2],
                     'GPIO': [bcolors.CGREEN, bcolors.CGREEN2]}
        if(func in colorFunc):
            color = colorFunc[func]
        if(self.debug):
            print(f"{bcolors.CEND}[{color[0]}{func}{bcolors.CEND}] {color[1]}{text}{bcolors.CEND}")

    def getReglage(self, nomGroupe, nomReglage, defaultValue = None):
        for g in self.reglages:
            if(self.reglages[g].nomCourt == nomGroupe):
                for r in self.reglages[g].reglages:
                    if(self.reglages[g].reglages[r].nomCourt == nomReglage):
                        self.log("getReglage", f"{nomGroupe}.{nomReglage} = {self.reglages[g].reglages[r].value}")
                        return self.reglages[g].reglages[r]

        self.log("getReglage", f"Impossible de trouver le réglage {nomReglage} du groupe {nomGroupe}. Ajoutez-le dans la BDD.")
        return Reglage(None, None, None, None, defaultValue)

    def newClient(self, client, server):
        client["data"] = {}
        client["data"]["editingStopPacket"] = None
        client["data"]["editingObject"] = None
        client["data"]["lastSentPercent"] = -1

    def clientLeft(self, client, server):
        packet = client["data"]["editingStopPacket"]
        editingObject = client["data"]["editingObject"]
        if(client == self.distributeur):
            self.distributeur = None
        if(packet != None):
            for other in self.ws.getOtherClients(client):
                self.ws.send_message(other, packet)
        if(editingObject != None):
            editingObject.editing = False

    def loadConfig(self):
        self.log('loadConfig', "Chargement de la configuration...")
        try:
            with open(os.path.join(application_path, 'config.json')) as json_file:
                self.config = json.load(json_file)
                self.log('loadConfig', "Configuration chargée")
        except Exception as e:
            self.log('loadConfig', "Erreur lors du chargement de la configuration, fermeture.")
            print(str(e))
            sys.exit(0)

    def message_received(self, client, server, msg):
        try:
            self.parser.parse(client, server, msg)
        except errors.ArgumentError as e:
            self.ws.send_message(client, "error|warning|L'argument suivant est invalide : " + str(e.text))
        except errors.ExceptionInfo as e:
            self.ws.send_message(client, "error|info|" + str(e.text))
        except Exception as e:
            self.ws.send_message(client, "error|danger|" + str(e))
            if(self.debug):
                traceback.print_exc()

    def sendCuves(self, client):
        for i in self.cuves:
            self.ws.send_message(client, self.cuves[i].addPacket())
        self.ws.send_message(client, "animation|cuves")

    def sendBoissons(self, client):
        for i in self.boissons:
            self.ws.send_message(client, self.boissons[i].addPacket())

    def sendReglages(self, client):
        for g in self.reglages:
            self.ws.send_message(client, self.reglages[g].addPacket())
            for r in self.reglages[g].reglages:
                self.ws.send_message(client, self.reglages[g].reglages[r].addPacket())

    def setupDistributeur(self, client):
        if(self.distributeur is not None):
            self.log('setupDistributeur', "Déconnexion de l'ancien distributeur...")
            self.ws.kickClient(self.distributeur)
        self.log('setupDistributeur', "Distributeur connecté")
        self.distributeur = client
        self.ws.send_message(client, "themeColor|"+self.reglageThemeCouleur.valueToString())

    def getAvailableBoissons(self):
        boissons = []

        for i in self.cuves:
            c = self.cuves[i]
            if(not c.enabled):
                continue
            boissons.append(c.boisson)

        return boissons

    def getCuveFromBoisson(self, boisson):
        for i in self.cuves:
            if(self.cuves[i].boisson == boisson):
                return self.cuves[i]

    def addService(self, boisson, quantite):
        cuve = self.getCuveFromBoisson(boisson)
        new = Service(boisson, cuve, quantite)
        self.services.append(new)

    def startMenu(self):
        self.log("startMenu", "Composition du service :")
        for service in self.services:
            self.log("startMenu", f" - {service.boisson.nomAffichage} : {service.quantiteService}Cl")
        if(self.distributeur != None):
            self.ws.send_message(self.distributeur, "distribution|start")

    def updateMenu(self):
        quantiteMax = 0
        quantiteRestant = 0

        for service in self.services:
            quantiteMax += service.quantiteService
            quantiteRestant += service.quantiteRestant

        if(self.distributeur != None):
            percent = 100-(quantiteRestant*100.0/quantiteMax)
            if(int(self.distributeur["data"]["lastSentPercent"]) != int(percent)):
                self.distributeur["data"]["lastSentPercent"] = int(percent)
                self.ws.send_message(self.distributeur, "percentDistribution|"+str(int(percent)))
                if(int(percent) == 100):
                    self.ws.send_message(self.distributeur, "distribution|stop")


    def onThemeCouleurChange(self, reglage, oldValue, newValue):
        if(self.distributeur != None):
            self.ws.send_message(self.distributeur, "themeColor|"+reglage.valueToString())

bar = Bartender()

while 1:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

bar.exit()
