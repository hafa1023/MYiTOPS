"""
KY040 Code form Martin O'Hanlon and Conrad Storz 
stuffaboutcode.com

Additional code added by Ferhat Aslan (University of Applied Science)
"""

import RPi.GPIO as GPIO
from time import sleep


class MYiTOPS:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    DEBOUNCE = 20

    def __init__(self, clockPin, dataPin, switchPin, laverSwitchPin, pushbutton1Pin, pushbutton2Pin,
                 led1Pin, led2Pin, led3Pin, led4Pin, led5Pin, rotaryCallback, switchCallback,
                 pushbutton1Callback, pushbutton2Callback):
        
        GPIO.setmode(GPIO.BCM)
        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallback = rotaryCallback
        self.switchCallback = switchCallback
        self.laverSwitchPin = laverSwitchPin
        self.pushbutton1Pin = pushbutton1Pin
        self.pushbutton2Pin = pushbutton2Pin
        self.led1Pin = led1Pin
        self.led2Pin = led2Pin
        self.led3Pin = led3Pin
        self.led4Pin = led4Pin
        self.led5Pin = led5Pin
        self.pushbutton1Callback = pushbutton1Callback
        self.pushbutton2Callback = pushbutton2Callback

        self.loop = True

        #setup pins
        GPIO.setup(clockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dataPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        GPIO.setup(laverSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pushbutton1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pushbutton2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        GPIO.setup(led1Pin, GPIO.OUT)
        GPIO.setup(led2Pin, GPIO.OUT)
        GPIO.setup(led3Pin, GPIO.OUT)
        GPIO.setup(led4Pin, GPIO.OUT)
        GPIO.setup(led5Pin, GPIO.OUT)

    def start(self):
        GPIO.add_event_detect(self.clockPin, GPIO.FALLING, callback=self._clockCallback, bouncetime=self.DEBOUNCE)
        GPIO.add_event_detect(self.switchPin, GPIO.FALLING, callback=self._switchCallback, bouncetime=self.DEBOUNCE)    
        GPIO.add_event_detect(self.pushbutton1Pin, GPIO.FALLING, callback=self._pushbutton1Callback, bouncetime=self.DEBOUNCE)
        GPIO.add_event_detect(self.pushbutton2Pin, GPIO.FALLING, callback=self._pushbutton2Callback, bouncetime=self.DEBOUNCE)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)
        GPIO.remove_event_detect(self.pushbutton1Pin)
        GPIO.remove_event_detect(self.pushbutton2Pin)

    
    def _clockCallback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            self.rotaryCallback(GPIO.input(self.dataPin))
        """
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.rotaryCallback(self.ANTICLOCKWISE)
            else:
                self.rotaryCallback(self.CLOCKWISE)
        
        self.rotaryCallback(GPIO.input(self.dataPin))
        """

    def _switchCallback(self, pin):
        """
        if GPIO.input(self.switchPin) == 0:
            self.switchCallback()
        """
        self.switchCallback()
        
    def getLaverSwitch(self):
        return GPIO.input(self.laverSwitchPin)
 
        
    def _pushbutton1Callback(self, pin):
        self.pushbutton1Callback(pin)

    def _pushbutton2Callback(self, pin):
        self.pushbutton2Callback(pin)
        
    def setLed1(self, on):
        if on: 
            GPIO.output(self.led1Pin, GPIO.HIGH)
        else:
            GPIO.output(self.led1Pin, GPIO.LOW)
            
    def setLed2(self, on):
        if on: 
            GPIO.output(self.led2Pin, GPIO.HIGH)
        else:
            GPIO.output(self.led2Pin, GPIO.LOW)
    
    def setLed3(self, on):
        if on: 
            GPIO.output(self.led3Pin, GPIO.HIGH)
        else:
            GPIO.output(self.led3Pin, GPIO.LOW)
            
    def setLed4(self, on):
        if on: 
            GPIO.output(self.led4Pin, GPIO.HIGH)
        else:
            GPIO.output(self.led4Pin, GPIO.LOW)
            
    def setLed5(self, on):
        if on: 
            GPIO.output(self.led5Pin, GPIO.HIGH)
        else:
            GPIO.output(self.led5Pin, GPIO.LOW)
        
    def setExit(self):
        print("exit")
        self.loop = False
        
    def getExit(self):
        print (self.loop)
        return self.loop

#test
if __name__ == "__main__":

    print ('Program start.')

    CLOCKPIN = 27
    DATAPIN = 22
    SWITCHPIN = 17
    LAVERSWITCH = 13
    PUSHBUTTON1 = 6
    PUSHBUTTON2 = 5
    LED1 = 18
    LED2 = 23
    LED3 = 24
    LED4 = 25
    LED5 = 12

    def rotaryChange(direction):
        print ("turned - " + str(direction))
    def switchPressed(pin):
        print ("button connected to pin:{} pressed".format(pin))
        
    def pushbutton1(pin):
        MYiTOPS.setExit()
        
    def pushbutton2(pin):
        pass

    
    MYiTOPS = MYiTOPS(CLOCKPIN, DATAPIN, SWITCHPIN, LAVERSWITCH, PUSHBUTTON1, PUSHBUTTON2, LED1, LED2, LED3, LED4, LED5,
                      rotaryChange, switchPressed, pushbutton1, pushbutton2)

    print ('Launch switch monitor class.')

    MYiTOPS.start()
    print ('Start program loop...')
    
    try:
        while MYiTOPS.getExit():
            #print(ky040.loopControl())
            sleep(1)
            MYiTOPS.setLed1(MYiTOPS.getLaverSwitch())
            print ('Ten seconds...')
            
    finally:
        print ('Stopping GPIO monitoring...')
        MYiTOPS.stop()
        GPIO.cleanup()
        print ('Program ended.')

