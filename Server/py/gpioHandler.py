# -*- coding: utf-8 -*-

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    from fake_rpigpio import RPi
    GPIO = RPi.GPIO

class GPIOHandler():
    def __init__(self, bartender):
        self.bartender = bartender
        self.indexPinDebitmetre = {}

    def load(self):
        self.bartender.log("GPIO", "Initialisation...")
        GPIO.setmode(GPIO.BOARD)

        for i in self.bartender.cuves:
            try:
                cuve = self.bartender.cuves[i]
                self.setupPinDebitmetre(cuve, cuve.debitmetrePinId)
            except Exception as e:
                self.bartender.log("GPIO", f"Impossible de configurer le pin {cuve.debitmetrePinId} en input... (débitmètre)")
                print(e)

    def stop(self):
        self.bartender.log("GPIO", "Nettoyage des ports GPIO...")
        GPIO.cleanup()

    def tickEvent(self, pin):
        cuve = self.indexPinDebitmetre[int(pin)]
        cuve.quantite -= cuve.debitmetreMlParTick
        if(int(cuve.quantite)%5==0):
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
