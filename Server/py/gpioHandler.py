# -*- coding: utf-8 -*-

import threading
import time

isRpi = True

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    from fake_rpigpio import RPi
    GPIO = RPi.GPIO
    isRpi = False

class GPIOHandler():
    def __init__(self, bartender):
        self.bartender = bartender
        self.indexPinDebitmetre = {}
        self.indexPinPompe = {}
        self.lastSentCuveQuantite = {}

    def load(self):
        self.bartender.log("GPIO", "Initialisation...")

        self.pinR = self.bartender.getReglage("BANDE_LED", "PIN_ROUGE", 0)
        self.pinR.eventHandler = self.onPinRChange
        self.pinG = self.bartender.getReglage("BANDE_LED", "PIN_VERT", 0)
        self.pinG.eventHandler = self.onPinGChange
        self.pinB = self.bartender.getReglage("BANDE_LED", "PIN_BLEU", 0)
        self.pinB.eventHandler = self.onPinBChange

        GPIO.setmode(GPIO.BOARD)

        for i in self.bartender.cuves:
            try:
                cuve = self.bartender.cuves[i]
                self.setupPinDebitmetre(cuve, cuve.debitmetrePinId)
                self.setupPinPompe(cuve, cuve.pompePinId)
            except Exception as e:
                self.bartender.log("GPIO", f"Impossible de configurer le pin {cuve.debitmetrePinId} en input... (débitmètre)")
                print(e)

        try:
            self.bartender.log("GPIO", f"Ajout du pin {self.pinR.value} en input... (pinR)")
            GPIO.setup(self.pinR.value, GPIO.OUT)
        except Exception as e:
            self.bartender.log("GPIO", f"Impossible de configurer le pin {self.pinR.value} en output... (pinR)")
            print(e)

        try:
            self.bartender.log("GPIO", f"Ajout du pin {self.pinG.value} en input... (pinG)")
            GPIO.setup(self.pinG.value, GPIO.OUT)
        except Exception as e:
            self.bartender.log("GPIO", f"Impossible de configurer le pin {self.pinG.value} en output... (pinG)")
            print(e)

        try:
            self.bartender.log("GPIO", f"Ajout du pin {self.pinB.value} en input... (pinB)")
            GPIO.setup(self.pinB.value, GPIO.OUT)
        except Exception as e:
            self.bartender.log("GPIO", f"Impossible de configurer le pin {self.pinB.value} en output... (pinB)")
            print(e)

        self.stopThread = False
        if(not isRpi):
            threading.Thread(target=self.fakeDistribution).start()

    def stop(self):
        self.bartender.log("GPIO", "Nettoyage des ports GPIO...")
        GPIO.cleanup()
        self.stopThread = True

    def tickEvent(self, pin):
        cuve = self.indexPinDebitmetre[int(pin)]
        if((cuve.quantite - cuve.debitmetreMlParTick)>=0):
            cuve.quantite -= cuve.debitmetreMlParTick
        else:
            cuve.quantite = 0

        cuve.quantite = round(cuve.quantite, 4)

        for service in self.bartender.services:
            if(service.cuve == cuve):
                service.quantiteRestant -= cuve.debitmetreMlParTick
                self.bartender.updateMenu()

        if(cuve not in self.lastSentCuveQuantite):
            self.lastSentCuveQuantite[cuve] = int(cuve.quantite)

        if(int(cuve.quantite) != self.lastSentCuveQuantite[cuve]):
            self.lastSentCuveQuantite[cuve] = int(cuve.quantite)
            self.bartender.ws.send_message_to_all(cuve.updatePacket())

    def setupPinDebitmetre(self, cuve, pin):
        self.bartender.log("GPIO", f"Ajout du pin {pin} en input... (débitmètre)")
        GPIO.setup(int(pin), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(int(pin), GPIO.FALLING, callback=self.tickEvent)
        self.indexPinDebitmetre[int(pin)] = cuve

    def unsetupPinDebitmetre(self, cuve, pin):
        self.bartender.log("GPIO", f"Suppression du pin {pin} en input... (débitmètre)")
        GPIO.remove_event_detect(pin)
        GPIO.cleanup(pin)
        del self.indexPinDebitmetre[int(pin)]

    def setupPinPompe(self, pompe, pin):
        self.bartender.log("GPIO", f"Ajout du pin {pin} en output... (pompe)")
        GPIO.setup(int(pin), GPIO.OUT)
        self.indexPinPompe[int(pin)] = pompe

    def unsetupPinPompe(self, pompe, pin):
        self.bartender.log("GPIO", f"Suppression du pin {pin} en output... (pompe)")
        GPIO.remove_event_detect(pin)
        GPIO.cleanup(pin)
        del self.indexPinPompe[int(pin)]

    def onPinRChange(self, reglage, oldValue, newValue):
        pass

    def onPinGChange(self, reglage, oldValue, newValue):
        pass

    def onPinBChange(self, reglage, oldValue, newValue):
        pass

    def fakeDistribution(self):
        self.bartender.log("GPIO", f"Démarrage de la fausse distribution...")
        while not self.stopThread:
            time.sleep(0.005)
            for service in self.bartender.services:
                if(service.quantiteRestant > 0):
                    self.tickEvent(service.cuve.debitmetrePinId)
        self.bartender.log("GPIO", f"Arrêt de la fausse distribution...")
