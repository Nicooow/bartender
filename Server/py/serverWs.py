# -*- coding: utf-8 -*-
#https://github.com/Pithikos/python-websocket-server

import logging
import threading, time
from websocket_server import WebsocketServer

class ServerWs(threading.Thread):
    def __init__(self, bartender):
        threading.Thread.__init__(self)
        self.bartender = bartender
        self.bartender.log("ServerWs", "Initialisation...")

    def run(self):
        self.bartender.log("ServerWs", f"Démarrage du serveur websocket sur l'adresse {self.bartender.wsIp}:{self.bartender.wsPort}...")
        self.server = WebsocketServer(self.bartender.wsPort, host=self.bartender.wsIp, loglevel=logging.NOTSET)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

    def send_message(self, client, msg):
        self.bartender.log("ServerWs", f"Envoie (id:{client['id']}) : {msg}")
        self.server.send_message(client, msg)

    def message_received(self, client, server, msg):
        self.bartender.log("ServerWs", f"Reçu (id:{client['id']}) : {msg}")
        self.bartender.message_received(client, server, msg)

    def new_client(self, client, server):
        self.bartender.log("ServerWs", f"Nouvelle connexion (id:{client['id']})")
        self.send_message(client, "page|accueil")
