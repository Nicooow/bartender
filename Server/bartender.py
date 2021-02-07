# -*- coding: utf-8 -*-

from py import parser, serverWs, bdd, errors
from py.bcolors import bcolors
import json

class Bartender():
    def __init__(self, debug = True):
        # PARAM
        self.debug = debug

        # MODULES
        self.bdd = bdd.BDD(self)
        self.parser = parser.Parser(self)
        self.ws = serverWs.ServerWs(self)

        # DONNEES
        self.boissons = {}
        self.cuves = {}
        self.config = {}

        # INIT
        self.log('__init__', "Initialisation...")
        self.loadConfig()
        self.bdd.connect()
        self.bdd.load()
        self.ws.start()

    def log(self, func, text):
        color = ["", ""];
        maxLength = 100
        text = text[:maxLength] + ("..." if len(text)>maxLength else "")
        colorFunc = {'ServerWs' : [bcolors.CYELLOW, bcolors.CYELLOW2],
                     'Parser' : [bcolors.CVIOLET, bcolors.CVIOLET2],
                     'Bdd' : [bcolors.CBLUE, bcolors.CBLUE2]}
        if(func in colorFunc):
            color = colorFunc[func]
        if(self.debug):
            print(f"{bcolors.CEND}[{color[0]}{func}{bcolors.CEND}] {color[1]}{text}{bcolors.CEND}")

    def newClient(self, client, server):
        client["data"] = {}
        client["data"]["editingStopPacket"] = None
        client["data"]["editingObject"] = None

    def clientLeft(self, client, server):
        packet = client["data"]["editingStopPacket"]
        editingObject = client["data"]["editingObject"]
        if(packet != None):
            for other in self.ws.getOtherClients(client):
                self.ws.send_message(other, packet)
        if(editingObject != None):
            editingObject.editing = False

    def loadConfig(self):
        self.log('loadConfig', "Chargement de la configuration...")
        try:
            with open('config.json') as json_file:
                self.config = json.load(json_file)
                self.log('loadConfig', "Configuration chargée")
        except Exception as e:
            self.log('loadConfig', "Erreur lors du chargement de la configuration, fermeture.")
            print(str(e))
            import sys
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

    def sendCuves(self, client):
        for i in self.cuves:
            cuve = self.cuves[i]
            packet = []
            packet.append("addElement")
            packet.append("cuve")
            packet.append(str(cuve.id))
            if(cuve.boisson == None):
                packet.append("?")
                packet.append("#fff")
            else:
                packet.append(cuve.boisson.nomCourt)
                packet.append(cuve.boisson.couleur)
            packet.append(str(int( (100-(cuve.quantitee*100/cuve.quantiteeMax))/100*250 )))
            self.ws.send_message(client, "|".join(packet))
        self.ws.send_message(client, "animation|cuves")

    def sendBoissons(self, client):
        for i in self.boissons:
            self.ws.send_message(client, self.boissons[i].addPacket())

Bartender()
