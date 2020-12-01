# -*- coding: utf-8 -*-
#https://github.com/Pithikos/python-websocket-server

import logging
import threading, time
from websocket_server import WebsocketServer

class serverWs(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.fn_message_received = None

    def run(self):
        self.server = WebsocketServer(12345, host='192.168.1.73', loglevel=logging.INFO)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.fn_message_received)
        self.server.run_forever()

    def new_client(self, client, server):
        print("newClient")
        #self.server.send_message(client, "page|accueil")
