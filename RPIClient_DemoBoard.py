"""
KY040 Code form Martin O'Hanlon and Conrad Storz 
stuffaboutcode.com

Additional code added by Ferhat Aslan (University of Applied Science)
"""

import RPi.GPIO as GPIO
from time import sleep
import socket
from PySide import QtNetwork, QtCore, QtGui
import _thread
GPIO.setmode(GPIO.BCM)

ipAdress = '192.168.178.20'

class MYiTOPS:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    DEBOUNCE = 20

    def __init__(self, clockPin, dataPin, switchPin, laverSwitchPin, pushbutton1Pin, pushbutton2Pin,
                 led1Pin, led2Pin, led3Pin, led4Pin, led5Pin, rotaryCallback, switchCallback,
                 pushbutton1Callback, pushbutton2Callback):
        
        
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
        self.switchCallback(pin)
        
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
        #print (self.loop)
        return self.loop

#test

if __name__ == "__main__":
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        print ("button connected to pin:{} pressed".format(pin))
    
        
    MYiTOPS = MYiTOPS(CLOCKPIN, DATAPIN, SWITCHPIN, LAVERSWITCH, PUSHBUTTON1, PUSHBUTTON2, LED1, LED2, LED3, LED4, LED5,
                      rotaryChange, switchPressed, pushbutton1, pushbutton2)

    print ('Launch switch monitor class.')

    MYiTOPS.start()
    print ('Start program loop...')
'''   
    def comToServer():
        try:
            on = '1'
            off = '0'      
            #name = "'RemoteRPIGroupN'"
            #header = "('Time Stamp', 'Hard key 1', 'Hard key 2', 'Hard key 3', 'KY-040-Encoder')"
            #values = " VALUES ('2018-12-22 14:09:36', 1, 0, 0, 123);"
            message = "'CHP- SenerTec Dachs G5.52' ('Time Stamp - Heat Meter 1', 'Th. Power [W] - Heat Meter 1', 'Water Flow [m^3/h] - Heat Meter 1', 'T_Flow [°C] - Heat Meter 1', 'T_Return [°C] - Heat Meter 1','Time Stamp - Heat Meter 2', 'Th. Power [W] - Heat Meter 2', 'Water Flow [m^3/h] - Heat Meter 2','T_Flow [°C] - Heat Meter 2', 'T_Return [°C] - Heat Meter 2') VALUES ('2018-02-23 14:09:36', 12000.2, 12.1258, 22.14, 22.44, '2018-12-11 14:09:36', 12000.1, 11.1258, 21.14, 21.44)"
            #message = "{} ({})".format(name, header + values)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((ipAdress, 50005))
            print ("Connection etaNet is done")
            block = QtCore.QByteArray()
            out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
            out.setVersion(QtCore.QDataStream.Qt_4_0)                                
            print(message)                    
            out.writeQString(message)             
            s.send(block.data())
            
            block2 = QtCore.QByteArray()
            into = QtCore.QDataStream(block2, QtCore.QIODevice.ReadWrite)
            into.setVersion(QtCore.QDataStream.Qt_4_0)
            #Die länge der erwarteten Nachicht sollte dynamisch sein!
            #Keine Sonderzeichen verwenden bzw. empfangen!!!! 
            message = s.recv(1024)
            byteMessageList = list(message)
            strMessage = ''.join(str(x) for x in byteMessageList)
            print(byteMessageList)
            print(strMessage)

            s.close()                    
        except:
               print ("NO Connection to etaNet. Please check your connection to server!")
    
    def boardThread():
        try:
            while MYiTOPS.getExit():
               sleep(0.2)
          #      MYiTOPS.setLed1(MYiTOPS.getLaverSwitch())
        except Exception as e:
            print ("Thread Board: ")

    def networkThread():
        try:
            while MYiTOPS.getExit():
               sleep(1)
           #     if(MYiTOPS.getLaverSwitch()):
            #        comToServer()
        except Exception as e:
            print ("Thread Network: ")
                                      
try:
    _thread.start_new_thread(boardThread, ())
    _thread.start_new_thread(networkThread, ())
except:
    print ("Error: unable to start thread")
'''
try:
    while MYiTOPS.getExit():
        sleep(0.2)
        status = MYiTOPS.getLaverSwitch()
        MYiTOPS.setLed1(status)
        MYiTOPS.setLed2(status)
        MYiTOPS.setLed3(status)
        MYiTOPS.setLed4(status)
        MYiTOPS.setLed5(status)
except:
            print ("Thread Board: ") 
 
finally:
    print ('Stopping GPIO monitoring...')
    MYiTOPS.stop()
    GPIO.cleanup()
    print ('Program ended.')
    