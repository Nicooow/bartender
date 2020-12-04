# -*- coding: utf-8 -*-

class Parser():
    def __init__(self, bartender):
        self.bartender = bartender
        self.bartender.log("Parser", "Initialisation...")

    def parse(self, client, server, msg):
        command = msg.split('|')[0]
        args = msg.split('|')[1:]

        self.bartender.log("Parser", f"Parse {command} : {', '.join(args)}")

        if(command == "ask"):
            if(args[0] == "cuves"):
                self.bartender.sendCuves(client)
            elif(args[0] == "boissons"):
                self.bartender.sendBoissons(client)
