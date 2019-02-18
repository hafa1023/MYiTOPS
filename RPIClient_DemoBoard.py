"""
KY040 Code form Martin O'Hanlon and Conrad Storz 
stuffaboutcode.com

Additional code added by Ferhat Aslan (University of Applied Science)
"""

'''
Please enter the IP address of the server here. Change the transfer rate if desired.
'''
ipAdress = '192.168.178.45'
# value in seconds
TRANSFERRATE = 1

import RPi.GPIO as GPIO
from time import sleep
import socket
from PySide import QtNetwork, QtCore, QtGui
import _thread
GPIO.setmode(GPIO.BCM)



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
        self.volume = 0
        self.push1 = False
        self.push2 = False
        self.laverSwitch = 0

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
    
    def getValues(self):
        return str(self.laverSwitch) + ", '"+ str(self.push1)+ "', '" + str(self.push2) + "', "+ str(self.volume)

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
            #self.rotaryCallback(GPIO.input(self.dataPin))
        
            data = GPIO.input(self.dataPin)
            if data == 0 and self.volume < 20:
                self.volume += 1
            elif data == 1 and self.volume > 0:
                self.volume -= 1
        print (self.volume)
        

    def _switchCallback(self, pin):
        self.volume = 0
        print ("Volume is set to zero.")
        print (self.volume)
        #self.switchCallback(pin)
        
    def getLaverSwitch(self):
        self.laverSwitch = GPIO.input(self.laverSwitchPin)
        return self.laverSwitch
 
        
    def _pushbutton1Callback(self, pin):
        if not GPIO.input(self.laverSwitchPin):
            self.pushbutton1Callback(pin)
        self.push1 = not self.push1
        print(self.push1)

    def _pushbutton2Callback(self, pin):
        #self.pushbutton2Callback(pin)
        self.push2 = not self.push2
        print(self.push2)
        
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
    
    byteMessageList = []
    values = "0, 0, 0, 0, 0"
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
   
    def comToServer(values):
        try:
            on = '1'
            off = '0'      
            header = "'MYiTOPS-RPI-Client3' ('Laver Switch', 'Push Button 1', 'Push Button 2', 'Encoder Volume') VALUES "
            message = "{} ({})".format(header, values)
            #message = "E5"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10.0)
            s.connect((ipAdress, 50005))
            #print ("Connection etaNet is done")
            block = QtCore.QByteArray()
            out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
            out.setVersion(QtCore.QDataStream.Qt_4_0)                                
            #print(message)                    
            out.writeQString(message)             
            s.send(block.data())
            
            block2 = QtCore.QByteArray()
            into = QtCore.QDataStream(block2, QtCore.QIODevice.ReadWrite)
            into.setVersion(QtCore.QDataStream.Qt_4_0)
            message = s.recv(1024)
            byteMessageList = list(message.decode('ascii'))
            strMessage = ''.join(str(x) for x in byteMessageList)
            #print(byteMessageList)
            #print(byteMessageList[5] + byteMessageList[7])
            #print(strMessage)
            s.close()
            return message
        except:
               print ("NO Connection to etaNet. Please check your connection to server!")
    
    def boardThread():
        try:
            MYiTOPS.setLed1(True)
            sleep(0.2)
            MYiTOPS.setLed1(False)
            MYiTOPS.setLed2(True)
            sleep(0.2)
            MYiTOPS.setLed2(False)
            MYiTOPS.setLed3(True)
            sleep(0.2)
            MYiTOPS.setLed3(False)
            MYiTOPS.setLed4(True)
            sleep(0.2)
            MYiTOPS.setLed4(False)
            MYiTOPS.setLed5(True)
            sleep(0.2)
            MYiTOPS.setLed5(False)
            while MYiTOPS.getExit():
                sleep(0.2)
                status = MYiTOPS.getLaverSwitch()
                if status:
                    MYiTOPS.setLed1(True)
                    sleep(0.2)
                    MYiTOPS.setLed1(False)


        except:
                    print ("Thread Board: ")
        finally:
            print ('Stopping GPIO monitoring...')
            MYiTOPS.stop()
            GPIO.cleanup()
            print ('Program ended.')
            _thread.exit_thread()

    def networkThread():
        try:
            while MYiTOPS.getExit():
                sleep(TRANSFERRATE)
                #print ("Network Thread is runing")
                if(MYiTOPS.getLaverSwitch()):
                    data = comToServer(MYiTOPS.getValues())
                    byteMessageList = list(data.decode('ascii'))
                    #print(byteMessageList)
                    
                    if byteMessageList[5] == 'E' and  byteMessageList[7] == '5':
                        pass

                    elif byteMessageList[5] == 'N':
                        print(byteMessageList[17])
                        
                        MYiTOPS.setLed5(int(byteMessageList[17]))
                        MYiTOPS.setLed2(int(byteMessageList[23]))
                        MYiTOPS.setLed3(int(byteMessageList[29]))
                        MYiTOPS.setLed4(int(byteMessageList[35]))
                        MYiTOPS.setLed5(int(byteMessageList[41]))
                    
                    else:
                        print("Wrong message! Please check your conection.")
                    
  
                      
                    
        except:
            print ("Thread Network: ")
        finally:
            print ('Stopping transfer of data')

        
MYiTOPS = MYiTOPS(CLOCKPIN, DATAPIN, SWITCHPIN, LAVERSWITCH, PUSHBUTTON1, PUSHBUTTON2, LED1, LED2, LED3, LED4, LED5,
                  rotaryChange, switchPressed, pushbutton1, pushbutton2)

print ('MYiTOPS Remote Control Client.')

MYiTOPS.start()

                                      
try:
    _thread.start_new_thread(boardThread, ())
    _thread.start_new_thread(networkThread, ())
except:
    print ("Error: unable to start thread")

#boardThread()
    