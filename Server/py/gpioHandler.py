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
        self.pompeOnByPin = []
        self.tickCountPompeByPin = {}
        self.alertPompeByPin = {}

    def load(self):
        self.bartender.log("GPIO", "Initialisation...")

        self.pinR = self.bartender.getReglage("BANDE_LED", "PIN_ROUGE", 0)
        self.pinR.eventHandler = self.onPinRChange
        self.PwmR = None
        self.pinG = self.bartender.getReglage("BANDE_LED", "PIN_VERT", 0)
        self.pinG.eventHandler = self.onPinGChange
        self.PwmG = None
        self.pinB = self.bartender.getReglage("BANDE_LED", "PIN_BLEU", 0)
        self.pinB.eventHandler = self.onPinBChange
        self.PwmB = None

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
            GPIO.output(self.pinR.value, GPIO.LOW)
            self.PwmR = GPIO.PWM(self.pinR.value, 100)
            self.PwmR.start(0)
        except Exception as e:
            self.bartender.log("GPIO", f"Impossible de configurer le pin {self.pinR.value} en output... (pinR)")
            print(e)

        try:
            self.bartender.log("GPIO", f"Ajout du pin {self.pinG.value} en input... (pinG)")
            GPIO.setup(self.pinG.value, GPIO.OUT)
            GPIO.output(self.pinG.value, GPIO.LOW)
            self.PwmG = GPIO.PWM(self.pinG.value, 100)
            self.PwmG.start(0)
        except Exception as e:
            self.bartender.log("GPIO", f"Impossible de configurer le pin {self.pinG.value} en output... (pinG)")
            print(e)

        try:
            self.bartender.log("GPIO", f"Ajout du pin {self.pinB.value} en input... (pinB)")
            GPIO.setup(self.pinB.value, GPIO.OUT)
            GPIO.output(self.pinB.value, GPIO.LOW)
            self.PwmB = GPIO.PWM(self.pinB.value, 100)
            self.PwmB.start(0)
        except Exception as e:
            self.bartender.log("GPIO", f"Impossible de configurer le pin {self.pinB.value} en output... (pinB)")
            print(e)

        self.stopThread = False
        if(not isRpi):
            threading.Thread(target=self.fakeDistribution).start()

        threading.Thread(target=self.securityThread).start()

    def stop(self):
        self.bartender.log("GPIO", "Nettoyage des ports GPIO...")
        self.PwmR.stop()
        self.PwmG.stop()
        self.PwmB.stop()
        GPIO.cleanup()
        self.stopThread = True

    def tickEvent(self, pin):
        cuve = self.indexPinDebitmetre[int(pin)]
        if((cuve.quantite - cuve.debitmetreMlParTick)>=0):
            cuve.quantite -= (cuve.debitmetreMlParTick/10)
        else:
            cuve.quantite = 0

        cuve.quantite = round(cuve.quantite, 4)

        for service in self.bartender.services:
            if(service.cuve == cuve):
                service.quantiteRestant -= (cuve.debitmetreMlParTick/10)
                self.bartender.updateMenu()

        if(cuve not in self.lastSentCuveQuantite):
            self.lastSentCuveQuantite[cuve] = int(cuve.quantite)

        if(int(cuve.quantite) != self.lastSentCuveQuantite[cuve]):
            self.lastSentCuveQuantite[cuve] = int(cuve.quantite)
            self.bartender.ws.send_message_to_all(cuve.updatePacket())

        if(int(cuve.pompePinId) in self.tickCountPompeByPin):
            self.tickCountPompeByPin[int(cuve.pompePinId)] += 1
        else:
            self.tickCountPompeByPin[int(cuve.pompePinId)] = 1

    def setupPinDebitmetre(self, cuve, pin):
        self.bartender.log("GPIO", f"Ajout du pin {pin} en input... (débitmètre)")
        GPIO.setup(int(pin), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
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
        GPIO.output(int(pin), GPIO.HIGH)
        self.indexPinPompe[int(pin)] = pompe

    def unsetupPinPompe(self, pompe, pin):
        self.bartender.log("GPIO", f"Suppression du pin {pin} en output... (pompe)")
        GPIO.output(int(pin), GPIO.HIGH)
        GPIO.remove_event_detect(int(pin))
        GPIO.cleanup(int(pin))
        del self.indexPinPompe[int(pin)]

    def onPinRChange(self, reglage, oldValue, newValue):
        pass

    def onPinGChange(self, reglage, oldValue, newValue):
        pass

    def onPinBChange(self, reglage, oldValue, newValue):
        pass

    def setRGB(self, r, g, b):
        self.PwmR.ChangeDutyCycle(r*100/255)
        self.PwmG.ChangeDutyCycle(g*100/255)
        self.PwmB.ChangeDutyCycle(b*100/255)

    def startPompe(self, pin):
        pin = int(pin)
        cuve = self.indexPinPompe[int(pin)]
        cuve.running = True
        self.bartender.ws.send_message_to_all(cuve.updatePacket())
        self.bartender.log("GPIO", f"Démarrage de la pompe {pin}...")
        GPIO.output(int(pin), GPIO.LOW)
        if(not pin in self.pompeOnByPin):
            self.pompeOnByPin.append(pin)
            self.tickCountPompeByPin[pin] = 0
            self.alertPompeByPin[pin] = 0

    def stopPompe(self, pin):
        pin = int(pin)
        cuve = self.indexPinPompe[int(pin)]
        cuve.running = False
        self.bartender.ws.send_message_to_all(cuve.updatePacket())
        self.bartender.log("GPIO", f"Arrêt de la pompe {pin}...")
        GPIO.output(int(pin), GPIO.HIGH)
        if(pin in self.pompeOnByPin):
            self.pompeOnByPin.remove(pin)
            del self.tickCountPompeByPin[pin]
            del self.alertPompeByPin[pin]

    def fakeDistribution(self):
        self.bartender.log("GPIO", f"Démarrage de la fausse distribution...")
        while not self.stopThread:
            time.sleep(0.0001)
            for service in self.bartender.services:
                if(service.quantiteRestant > 0):
                    for i in range(0,10):
                        self.tickEvent(service.cuve.debitmetrePinId)
        self.bartender.log("GPIO", f"Arrêt de la fausse distribution...")

    def securityThread(self):
        self.bartender.log("GPIO", f"Démarrage de la sécurité des pompes...")
        while not self.stopThread:
            time.sleep(1)
            for pin in self.pompeOnByPin:
                cuve = self.indexPinPompe[int(pin)]
                print("pompe on : " + str(pin))
                print(str(self.tickCountPompeByPin[int(pin)]*cuve.debitmetreMlParTick) + "mL/s")
                self.tickCountPompeByPin[int(pin)] = 0
        self.bartender.log("GPIO", f"Arrêt de la sécurité des pompes...")
