import RPi.GPIO as GPIO
import time
import socket
from PySide import QtNetwork, QtCore, QtGui
import threading 

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.IN)
print("init GBIOs")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(GPIO.input(11))
   

def comToServer():
    try:
        ipAdress = '192.168.178.20'
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

        #GPIO.output(12, not GPIO.input(12))    
while (not GPIO.input(11)):
    time.sleep(0.1)
    print("Stop Button:")
    print(GPIO.input(11))
comToServer()     