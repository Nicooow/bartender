# -*- coding: utf-8 -*-

from py import parser, serverWs, bdd
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
        self.pompes = {}
        self.debitmetres = {}
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
        colorFunc = {'ServerWs' : [bcolors.CYELLOW, bcolors.CYELLOW2],
                     'Parser' : [bcolors.CVIOLET, bcolors.CVIOLET2],
                     'Bdd' : [bcolors.CBLUE, bcolors.CBLUE2]}
        if(func in colorFunc):
            color = colorFunc[func]
        if(self.debug):
            print(f"{bcolors.CEND}[{color[0]}{func}{bcolors.CEND}] {color[1]}{text}{bcolors.CEND}")

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
        self.parser.parse(client, server, msg)

    def sendCuves(self, client):
        for cuves in self.cuves:
            pass
        self.ws.send_message(client, "addElement|cuve|1|Coca|#8A4C15|120")
        self.ws.send_message(client, "animation|cuves")

    def sendBoissons(self, client):
        self.ws.send_message(client, "addElement|boisson|Coca|https://stock.flashmode.tn/wp-content/uploads/2020/06/coca-cola-logo-png-100.png|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Jagermeister|https://lezebre.lu/images/detailed/16/22045-jagermeister-logo.png|#FF8000|35")
        self.ws.send_message(client, "addElement|boisson|Ice-Tea|https://freevectorlogo.net/wp-content/uploads/2013/03/ice-tea-lipton-vector-logo.png|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Redbull|https://cdn.freebiesupply.com/logos/large/2x/red-bull-logo-png-transparent.png|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Orangina|https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRam3ARjr4sPdKgDNZpHICoy6VlxvpFelx-Jw&usqp=CAU|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Clan Campbell|https://media.discordapp.net/attachments/328323448923488259/756193312435601549/clancampbell.png|#FF8000|40")



Bartender()
