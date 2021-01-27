# -*- coding: utf-8 -*-

from py.errors import ArgumentError

class Parser():
    def __init__(self, bartender):
        self.bartender = bartender
        self.bartender.log("Parser", "Initialisation...")

    def parse(self, client, server, msg):
        command = msg.split('|')[0]
        args = msg.split('|')[1:]
        idToUpdate = -1

        self.bartender.log("Parser", f"Parse {command} : {', '.join(args)}")

        if(command == "ask"):
            if(args[0] == "cuves"):
                self.bartender.sendCuves(client)
            elif(args[0] == "boissons"):
                self.bartender.sendBoissons(client)

        elif(command=="add" or command=="update"):
            if(command=="update"):
                idToUpdate = args[0]
                args = args[1:]
            if(args[0] == "boisson"):
                nomAffichage = args[1]
                nomCourt = args[2]
                couleur = args[3]
                try:
                    pourcentageAlcool = float(args[4].replace(',', "."))
                except:
                    raise ArgumentError("Pourcentage d'alcool de la boisson")
                logo = ''.join(args[5:])

                if(nomCourt==""):
                    raise ArgumentError("Nom court")
                if(nomAffichage==""):
                    raise ArgumentError("Nom complet")
                if(couleur==""):
                    raise ArgumentError("Couleur")

                if(idToUpdate==-1):
                    try:
                        newBoisson = self.bartender.bdd.newBoisson(nomAffichage, nomCourt, couleur, pourcentageAlcool, logo)
                        self.bartender.ws.send_message(client, "page|listBoissons")
                        for other in self.bartender.ws.getOtherClients(client):
                            self.bartender.ws.send_message(other, newBoisson.addPacket())
                    except Exception as e:
                        self.bartender.log("Bdd", f"Erreur lors de la création d'une boisson")
                        print(str(e))
                        raise e
                else:
                    try:
                        updateBoisson = self.bartender.bdd.updateBoisson(idToUpdate, nomAffichage, nomCourt, couleur, pourcentageAlcool, logo)
                        self.bartender.ws.send_message(client, "page|listBoissons")
                        for other in self.bartender.ws.getOtherClients(client):
                            self.bartender.ws.send_message(other, updateBoisson.updatePacket())
                    except Exception as e:
                        self.bartender.log("Bdd", f"Erreur lors de la modification d'une boisson")
                        print(str(e))
                        raise e
