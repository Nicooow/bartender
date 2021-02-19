# -*- coding: utf-8 -*-

from py.errors import ArgumentError, ExceptionInfo

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
            elif(args[0] == "updateBoisson"):
                try:
                    idAsk = int(args[1])
                    askedBoisson = self.bartender.boissons[idAsk]
                    self.bartender.ws.send_message(client, askedBoisson.updatePacket())
                except:
                    pass

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
                        self.bartender.log("Bdd", "Erreur lors de la création d'une boisson")
                        print(str(e))
                        raise e
                else:
                    try:
                        updateBoisson = self.bartender.bdd.updateBoisson(idToUpdate, nomAffichage, nomCourt, couleur, pourcentageAlcool, logo)
                        self.bartender.ws.send_message(client, "page|listBoissons")
                        for other in self.bartender.ws.getOtherClients(client):
                            self.bartender.ws.send_message(other, updateBoisson.updatePacket())
                    except Exception as e:
                        self.bartender.log("Bdd", "Erreur lors de la modification d'une boisson")
                        print(str(e))
                        raise e

            elif(args[0] == "cuve"):
                quantite = args[1]
                quantiteMax = args[2]
                pompePinId = args[3]
                dmPinId = args[4]
                dmMlParTick = args[5]
                bId = args[6]

                try:
                    quantite = float(quantite.replace(',', "."))
                except:
                    raise ArgumentError("Quantité actuelle (nombre incorrecte)")
                try:
                    pompePinId = int(pompePinId)
                except:
                    raise ArgumentError("Pin de la pompe (nombre incorrecte)")
                try:
                    dmPinId = int(dmPinId)
                except:
                    raise ArgumentError("Pin du débitmètre (nombre incorrecte)")
                try:
                    quantiteMax = float(quantiteMax.replace(',', "."))
                except:
                    raise ArgumentError("Quantité maximum (nombre incorrecte)")
                try:
                    dmMlParTick = float(dmMlParTick.replace(',', "."))
                except:
                    raise ArgumentError("Nombre de ML par Tick du débitmètre (nombre incorrecte)")
                try:
                    bId = int(bId)
                except:
                    raise ArgumentError("Boisson contenue (nombre incorrecte)")

                if(quantiteMax < quantite):
                    raise ArgumentError("La quantité maximum ne peut être inférieur à la quantitée actuelle")
                if(quantiteMax == 0):
                    raise ArgumentError("La quantité maximum ne peut être égale à 0")
                if(quantiteMax < 0 or quantite < 0):
                    raise ArgumentError("Une quantité ne peut être négative")
                if(dmMlParTick < 0):
                    raise ArgumentError("Le nombre de ML par Tick du débitmètre ne peut être négatif")
                if(pompePinId not in (2,5,7,8,10,11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40)):
                    raise ArgumentError("Le pin de la pompe n'est pas un port GPIO valable")
                if(dmPinId not in (2,5,7,8,10,11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40)):
                    raise ArgumentError("Le pin du débitmètre n'est pas un port GPIO valable")

                if(idToUpdate==-1):
                    try:
                        newCuve = self.bartender.bdd.newCuve(quantite, quantiteMax, pompePinId, dmPinId, dmMlParTick, bId)
                        self.bartender.ws.send_message(client, "page|listCuves")
                        for other in self.bartender.ws.getOtherClients(client):
                            self.bartender.ws.send_message(other, newCuve.addPacket())
                    except Exception as e:
                        self.bartender.log("Bdd", "Erreur lors de la création d'une cuve")
                        print(str(e))
                        raise e
                else:
                    try:
                        updateCuve = self.bartender.bdd.updateCuve(idToUpdate, quantite, quantiteMax, pompePinId, dmPinId, dmMlParTick, bId)
                        self.bartender.ws.send_message(client, "page|listCuves")
                        for other in self.bartender.ws.getOtherClients(client):
                            self.bartender.ws.send_message(other, updateCuve.updatePacket())
                    except Exception as e:
                        self.bartender.log("Bdd", "Erreur lors de la modification d'une cuve")
                        print(str(e))
                        raise e

        elif(command=="delete"):
            if(args[0] == "boisson"):
                idToDelete = args[1]
                try:
                    self.bartender.bdd.deleteBoisson(idToDelete)
                    self.bartender.ws.send_message_to_all("deleteElement|boisson|" + str(idToDelete))
                except Exception as e:
                    self.bartender.log("Bdd", "Erreur lors de la suppression d'une boisson")
                    print(str(e))
                    raise e
            if(args[0] == "cuve"):
                idToDelete = args[1]
                try:
                    self.bartender.bdd.deleteCuve(idToDelete)
                    self.bartender.ws.send_message_to_all("deleteElement|cuve|" + str(idToDelete))
                except Exception as e:
                    self.bartender.log("Bdd", "Erreur lors de la suppression d'une cuve")
                    print(str(e))
                    raise e

        elif(command=="editing"):
            if(args[0] == "boisson"):
                idEditing = args[1]
                isEditing = args[2]

                if(not int(idEditing) in self.bartender.boissons):
                    raise Exception("Boisson inexistante. Cette erreur n'est pas censée arriver.")

                editingBoisson = self.bartender.boissons[int(idEditing)]

                if((editingBoisson.editing == True) and (client["data"]["editingObject"] != editingBoisson)):
                    if(bool(int(isEditing))):
                        self.bartender.ws.send_message(client, "page|accueil")
                        raise Exception("Cette boisson est déjà en modification.")

                if(bool(int(isEditing))):
                    if(client["data"]["editingObject"] != None):
                        self.bartender.ws.send_message(client, "page|accueil")
                        raise Exception("Vous êtes déjà en train de modifier un élément.")
                    editingBoisson.editing = True
                    client["data"]["editingStopPacket"] = "editingElement|boisson|" + str(idEditing) + "|0"
                    client["data"]["editingObject"] = editingBoisson
                else:
                    editingBoisson.editing = False
                    if(client["data"]["editingObject"] != editingBoisson):
                        client["data"]["editingObject"].editing = False
                        for other in self.bartender.ws.getOtherClients(client):
                            self.bartender.ws.send_message(other, client["data"]["editingStopPacket"])
                        raise ExceptionInfo("Vous n'étiez pas censer modifier cet élément.")
                    client["data"]["editingStopPacket"] = None
                    client["data"]["editingObject"] = None

                for other in self.bartender.ws.getOtherClients(client):
                    self.bartender.ws.send_message(other, "editingElement|boisson|" + str(idEditing) + "|" + str(isEditing))

            if(args[0] == "cuve"):
                idEditing = args[1]
                isEditing = args[2]

                if(not int(idEditing) in self.bartender.cuves):
                    raise Exception("Cuve inexistante. Cette erreur n'est pas censée arriver.")

                editingCuve = self.bartender.cuves[int(idEditing)]

                if((editingCuve.editing == True) and (client["data"]["editingObject"] != editingCuve)):
                    if(bool(int(isEditing))):
                        self.bartender.ws.send_message(client, "page|accueil")
                        raise Exception("Cette cuve est déjà en modification.")

                if(bool(int(isEditing))):
                    if(client["data"]["editingObject"] != None):
                        self.bartender.ws.send_message(client, "page|accueil")
                        raise Exception("Vous êtes déjà en train de modifier un élément.")
                    editingCuve.editing = True
                    client["data"]["editingStopPacket"] = "editingElement|cuve|" + str(idEditing) + "|0"
                    client["data"]["editingObject"] = editingCuve
                else:
                    editingCuve.editing = False
                    if(client["data"]["editingObject"] != editingCuve):
                        client["data"]["editingObject"].editing = False
                        for other in self.bartender.ws.getOtherClients(client):
                            self.bartender.ws.send_message(other, client["data"]["editingStopPacket"])
                        raise ExceptionInfo("Vous n'étiez pas censer modifier cet élément.")
                    client["data"]["editingStopPacket"] = None
                    client["data"]["editingObject"] = None

                for other in self.bartender.ws.getOtherClients(client):
                    self.bartender.ws.send_message(other, "editingElement|cuve|" + str(idEditing) + "|" + str(isEditing))
