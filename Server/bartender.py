# -*- coding: utf-8 -*-

import sys
import json
import time
import traceback
from py import parser, serverWs, gpioHandler, bdd, errors
from py.bcolors import bcolors

class Bartender():
    def __init__(self, debug = True):
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

        # INIT
        self.log('__init__', "Initialisation...")
        self.loadConfig()
        self.bdd.connect()
        self.bdd.load()
        self.ws.daemon = True
        self.ws.start()
        self.gpio.load()

    def exit(self):
        self.bdd.disconnect()
        self.ws.close()
        self.gpio.stop()

    def log(self, func, text):
        color = ["", ""]
        maxLength = 100
        text = text[:maxLength] + ("..." if len(text)>maxLength else "")
        colorFunc = {'ServerWs' : [bcolors.CYELLOW, bcolors.CYELLOW2],
                     'Parser' : [bcolors.CVIOLET, bcolors.CVIOLET2],
                     'Bdd' : [bcolors.CBLUE, bcolors.CBLUE2],
                     'GPIO' : [bcolors.CGREEN, bcolors.CGREEN2]}
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

bar = Bartender()

while 1:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

bar.exit()
