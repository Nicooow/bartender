# -*- coding: utf-8 -*-
#https://github.com/Pithikos/python-websocket-server

import logging
import threading
from websocket_server import WebsocketServer

class ServerWs(threading.Thread):
    def __init__(self, bartender):
        threading.Thread.__init__(self)
        self.bartender = bartender
        self.bartender.log("ServerWs", "Initialisation...")
        self.server = None

    def run(self):
        self.bartender.log("ServerWs", f"Démarrage du serveur websocket sur l'adresse {self.bartender.config['ws']['ip']}:{self.bartender.config['ws']['port']}...")
        try:
            self.server = WebsocketServer(self.bartender.config["ws"]["port"], host=self.bartender.config["ws"]["ip"], loglevel=logging.NOTSET)
            self.server.set_fn_new_client(self.new_client)
            self.server.set_fn_message_received(self.message_received)
            self.server.set_fn_client_left(self.client_left)
            self.bartender.log("ServerWs", "Serveur démarré")
            self.server.run_forever()
        except Exception as e:
            self.bartender.log("ServerWs", "Erreur lors du démarrage du serveur : " + str(e))

    def close(self):
        self.bartender.log("ServerWs", "Arrêt du serveur websocket...")
        try:
            self.server.server_close()
            self.server = None
            self.bartender.log("ServerWs", "Arrêté")
        except Exception as e:
            self.bartender.log("ServerWs", "Erreur lors de l'arrêt du serveur : " + str(e))

    def send_message(self, client, msg):
        self.bartender.log("ServerWs", f"Envoie (id:{client['id']}) : {msg}")
        self.server.send_message(client, msg)

    def send_message_to_all(self, msg):
        self.bartender.log("ServerWs", f"Envoie (all) : {msg}")
        self.server.send_message_to_all(msg)

    def message_received(self, client, server, msg):
        self.bartender.log("ServerWs", f"Reçu (id:{client['id']}) : {msg}")
        self.bartender.message_received(client, server, msg)

    def new_client(self, client, server):
        self.bartender.log("ServerWs", f"Nouvelle connexion (id:{client['id']})")
        self.bartender.newClient(client, server)

    def client_left(self, client, server):
        self.bartender.log("ServerWs", f"Déconnexion (id:{client['id']})")
        self.bartender.clientLeft(client, server)

    def getOtherClients(self, client):
        clients = []
        for other in self.server.clients:
            if(other!=client):
                clients.append(other)
        return clients
