# -*- coding: utf-8 -*-

from py import parser, serverWs

class Bartender():
    def __init__(self, debug = True):
        # PARAM
        self.debug = debug
        self.wsIp = "192.168.1.73"
        self.wsPort = 12345

        # MODULES
        self.parser = parser.Parser(self)
        self.ws = serverWs.ServerWs(self)

        # INIT
        self.log('__init__', "Initialisation...")
        self.ws.start()

    def log(self, func, text):
        if(self.debug):
            print(f"[{func}] {text}")

    def message_received(self, client, server, msg):
        self.parser.parse(client, server, msg)

    def sendCuves(self, client):
        self.ws.send_message(client, "addElement|cuve|1|Coca|#8A4C15|120")
        self.ws.send_message(client, "addElement|cuve|2|Orange|#FF8000|40")
        self.ws.send_message(client, "addElement|cuve|3|Vodka|#E4E4E4|70")
        self.ws.send_message(client, "addElement|cuve|4|Whisky|#521E1E|110")
        self.ws.send_message(client, "addElement|cuve|5|Get27|#06AF06|20")
        self.ws.send_message(client, "addElement|cuve|6|Eau|#0FA4F9|50")
        self.ws.send_message(client, "animation|cuves")

    def sendBoissons(self, client):
        self.ws.send_message(client, "addElement|boisson|Coca|https://stock.flashmode.tn/wp-content/uploads/2020/06/coca-cola-logo-png-100.png|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Jagermeister|https://lezebre.lu/images/detailed/16/22045-jagermeister-logo.png|#FF8000|35")
        self.ws.send_message(client, "addElement|boisson|Ice-Tea|https://freevectorlogo.net/wp-content/uploads/2013/03/ice-tea-lipton-vector-logo.png|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Redbull|https://cdn.freebiesupply.com/logos/large/2x/red-bull-logo-png-transparent.png|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Orangina|https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRam3ARjr4sPdKgDNZpHICoy6VlxvpFelx-Jw&usqp=CAU|#FF8000|0")
        self.ws.send_message(client, "addElement|boisson|Clan Campbell|https://media.discordapp.net/attachments/328323448923488259/756193312435601549/clancampbell.png|#FF8000|40")



Bartender()
