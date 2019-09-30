"""
MYiTOPSGermany
Python Subteam
Autoren : Danial Haris Bin Limi Hawari, Fabian Harlacher

Script zur Steuerung der Aktorik der Höhen- und Klimakammer des IKKU in Bruchsal per Datenbank


"""

import pigpio
from enum import Enum
from time import sleep
from time import time
import mysql.connector
from mysql.connector import errorcode
import threading


    
# Klasse Sevo zum einbinden von pigpio und Fahren mit integrierter Winkel zu Pulsweiteumrechnung / Gassteuerung
class Servo:
    def __init__(self, pi, GPIO, Nullposition = 1500, min_Winkel = -20,anschlag_Winkel = 0, max_Winkel = 20):   # Nullpostion gibt die Mittelstellung in Pulsweite an, durch Tests bestimmt
        self.GPIO = GPIO
        self.Nullposition = Nullposition
        self.min_Winkel = min_Winkel
        self.anschlag_Winkel = anschlag_Winkel
        self.max_Winkel = max_Winkel
        self.Prozent = 0
        
        self.Servo_Lib = pi
        
    def move(self, Winkel): # Bewegen mit Winkel, Umrechnung auf Pulsweite
        self.Servo_Lib.set_servo_pulsewidth(self.GPIO, self.Nullposition + (Winkel * 10))
        self.Position = Winkel
        
    def gas_prozent(self, prozent): # Gassteuerung
        self.Prozent = prozent
        self.Position = self.anschlag_Winkel + (prozent*(self.max_Winkel-self.anschlag_Winkel))/100
        self.Servo_Lib.set_servo_pulsewidth(self.GPIO, self.Nullposition + self.Position * 10)
       
    def ausschalten(self):
        self.Servo_Lib.set_servo_pulsewidth(self.GPIO, 0)
       
class Kaltstart_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Kaltstart Thread wird gestartet")
        
    def run(self):
        global Kaltstart_Flag
        global Warmstart_Flag
        global Betrieb_Flag
        global ChangeMode_Flag
        
        if Warmstart_Flag:
            print("Warmstart eingestellt, umstellen auf Kaltstart")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Warmstart)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
        elif Betrieb_Flag:
            print("Betrieb eingestellt, umstellen auf Kaltstart")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Betrieb)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_max)
            print("Gas drücken")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
            print("Hebel auf Kaltstart")
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_min)
            print("Gas auf min")
            
        else:
            print("Kaltstart einstellen")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_aus)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            print("Hebel ausfahren")
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_max)
            print("Gas drücken")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
            print("Hebel auf Kaltstart")
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_min)
            print("Gas auf min")

        sleep(0.5)
        Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
        print("Hebel einfahren")
        sleep(0.1)
        #Ein wenig zurückfahren weil Einfahren hängt
        Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren+1)
        print("Kaltstart eingestellt")
        
        Warmstart_Flag = False
        Betrieb_Flag = False
        Kaltstart_Flag = True
        ChangeMode_Flag = False
        
        print("Kaltstart Thread wird geschlossen")
        return
        
        
        
       
class Warmstart_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Warmstart Thread wird gestartet")
        
    def run(self):
        global Kaltstart_Flag
        global Warmstart_Flag
        global Betrieb_Flag
        global ChangeMode_Flag
        
        if Kaltstart_Flag:
            print("Kaltstart eingestellt, umstellen auf Warmstart")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Warmstart)
        
        elif Betrieb_Flag:
            print("Betrieb eingestellt, umstellen auf Warmstart")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Betrieb)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_max)
            print("Gas drücken")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
            print("Hebel auf Kaltstart")
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_min)
            print("Gas auf min")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Warmstart)
            print("Hebel auf Warmstart")
            
            
        else:
            print("Warmstart einstellen")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_aus)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            print("Hebel ausfahren")
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_max)
            print("Gas drücken")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
            print("Hebel auf Kaltstart")
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_min)
            print("Gas auf min")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Warmstart)
            print("Hebel auf Warmstart")
        
        sleep(0.5)
        Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
        print("Hebel einfahren")
        sleep(0.1)
        #Ein wenig zurückfahren weil Einfahren hängt
        Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren+1)
        print("Warmstart eingestellt")
        
        Kaltstart_Flag = False
        Betrieb_Flag = False
        Warmstart_Flag = True
        
        ChangeMode_Flag = False
        
        print("Warmstart Thread wird geschlossen")
        return
        

class Betrieb_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Betrieb Thread wird gestartet")
        
    def run(self):
        global Kaltstart_Flag
        global Warmstart_Flag
        global Betrieb_Flag
        global ChangeMode_Flag
        
        if Kaltstart_Flag:
            print("Kaltstart eingestellt, umstellen auf Betrieb")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Warmstart)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
            print("Hebel einfahren")
            sleep(0.1)
            #Ein wenig zurückfahren weil Einfahren hängt
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren+1)
            Gas_Servo.move(Winkel_Gas_max)
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_min)
            print("Betrieb eingestellt")        
            
        elif Warmstart_Flag:
            print("Warmstart eingestellt, umstellen auf Betrieb")
            Gas_Servo.move(Winkel_Gas_max)
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_min)
            print("Betrieb eingestellt")
        
        else:
            print("Betrieb einstellen")
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_aus)
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            print("Hebel ausfahren")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Betrieb)
            print("Hebel auf Betrieb")
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
            print("Hebel einfahren")
            sleep(0.1)
            #Ein wenig zurückfahren weil Einfahren hängt
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren+1)
            print("Betrieb eingestellt")
     
        Kaltstart_Flag = False
        Warmstart_Flag = False
        Betrieb_Flag = True
        
        ChangeMode_Flag = False
        print("Betrieb Thread wird geschlossen")
        return

class Motor_stopp_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Betrieb Thread wird gestartet")
        
    def run(self):
        global Motor_an_Flag
        global Kaltstart_Flag
        global Warmstart_Flag
        global Betrieb_Flag
        global ChangeMode_Flag
        


        if Betrieb_Flag:
            Gas_Servo.move(Winkel_Gas_min)
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Betrieb)
            print("Drehen Betrieb")
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            print("Ausfahren")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_aus)
            print("Drehen Aus")
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
            print("Einfahren")
            
        elif Warmstart_Flag:
            Gas_Servo.move(Winkel_Gas_max)
            sleep(0.5)
            Gas_Servo.move(Winkel_Gas_min)
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Betrieb)
            print("Drehen Betrieb")
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            print("Ausfahren")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_aus)
            print("Drehen Aus")
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
            print("Einfahren")
            
        elif Kaltstart_Flag:
            Gas_Servo.move(Winkel_Gas_min)
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_Kaltstart)
            print("Drehen Betrieb")
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_ausfahren)
            print("Ausfahren")
            sleep(0.5)
            Chokehebel_drehen_Servo.move(Winkel_Chokehebel_aus)
            print("Drehen Aus")
            sleep(0.5)
            Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
            print("Einfahren")
            
            
        Kaltstart_Flag = False
        Warmstart_Flag = False
        Betrieb_Flag = False
        ChangeMode_Flag = False
        print("Motor gestoppt")

class frequence_Thread(threading.Thread):
        def __init__(self, pi, gpio, frequencedivider = 1):
            threading.Thread.__init__(self)
            print("Frequenz Thread wird gestartet")
            
            self.pi = pi
            self._tick = 0
            
            self.frequencelistlength = 10
            self.frequencelist = [0]*self.frequencelistlength
            self.frequencedivider = frequencedivider
            self.frequence = 0
            self.averagefrequence = 0
            self.RPM = 0
            self.Timer = time()
            self.last_tick = 0
            self.pi.set_mode(gpio, pigpio.INPUT)
            
            self._cb = self.pi.callback(gpio, pigpio.RISING_EDGE, self._cbf)
            
        def run(self):
            while True:
                self.diff = time()- self.Timer
                if self.last_tick + 0.15 < time():
                    self.frequencelist.insert(0, 0)
                    self.frequencelist.pop()
                sum = 0
                l = self.frequencelist
                for i in range(0,self.frequencelistlength):
                    sum += l[i]
                    
                self.averagefrequence = sum/self.frequencelistlength
                self.RPM = self.averagefrequence*60*self.frequencedivider        
        def _cbf(self, gpio, level, tick):
            self.last_tick = time()
            t = tick-self._tick
            self.frequence = (1000000.00/t)
            self.frequencelist.insert(0, self.frequence)
            self.frequencelist.pop()
            self._tick = tick
        
        def cancel(self):
            self._cb.cancel()
            
class Not_Aus_class:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.pi.set_mode(gpio, pigpio.INPUT)
        self.pi.set_glitch_filter(gpio, 10000)
        self._cb = self.pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)
        
    def _cbf(self, gpio, level, tick):
        global Motor_an_Flag
        global Not_Aus_Flag
        global Kaltstart_Flag
        global Warmstart_Flag
        global Betrieb_Flag
        global Gas_Relais_GPIO
        global Chokehebel_fahren_Relais_GPIO
        global Chokehebel_drehen_Relais_GPIO
        global Zustand
        
        #Not aus betätigt
        if level == 0:
            Not_Aus_Flag = True
            Motor_an_Flag = False
            print("Notaus betätigt\n----------------WICHTIG----------------\nVor Lösen des Notaus Chokehebel auf 0 stellen!")
            Gas_Servo.ausschalten()
            Chokehebel_fahren_Servo.ausschalten()
            Chokehebel_drehen_Servo.ausschalten()
            pi.write(Gas_Relais_GPIO, 0)
            pi.write(Chokehebel_fahren_Relais_GPIO, 0)
            pi.write(Chokehebel_drehen_Relais_GPIO, 0)
            LED_off()
            Zustand = Zustaende.Aus
            Kaltstart_Flag = False
            Warmstart_Flag = False
            Betrieb_Flag = False
                 
        if level == 1:
            sleep(2) #Sichergehen dass die BewegungsThreads geschlossen sind
            
            Relais_Setup()
            Grundstellung()
            
            Not_Aus_Flag = False
            print("Notaus gelöst")    
            
    def cancel(self):
        self._cb.cancel()
  
class Zustaende(Enum):
    
    Aus = "'Aus'"
    Betrieb = "'Betrieb'"
    Warmstart = "'Warmstart'"
    Kaltstart = "'Kaltstart'"
            
def Relais_Setup():
    global Gas_Relais_GPIO
    global Chokehebel_fahren_Relais_GPIO
    global Chokehebel_drehen_Relais_GPIO
        
    pi.write(Gas_Relais_GPIO, 1)
    print("Gas Relais zugeschalten")
    sleep(0.5)
    pi.write(Chokehebel_fahren_Relais_GPIO, 1)
    print("Chokehebel fahren Relais zugeschalten")
    sleep(0.5)
    pi.write(Chokehebel_drehen_Relais_GPIO, 1)
    print("Chokehebel drehen Relais zugeschalten")  
    
# Grundstellung anfahren
def Grundstellung():
    print("Grundstellung wird angefahren")
    sleep(0.5)
    Gas_Servo.move(Winkel_Gas_min)
    Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren)
    sleep(0.2)
    Chokehebel_fahren_Servo.move(Winkel_Chokehebel_einfahren+1) # Rohr hängt, ein bisschen zurückfahren
    sleep(0.5) # Warten bis Chokehebel eingefahren ist bevor gedreht wird
    Chokehebel_drehen_Servo.move(Winkel_Chokehebel_aus)
    print("Grundstellung angefahren")
    sleep(2)

# Datenbank verbindung
def db_connection():
    global connection_counter
    connection_counter = 0
    while True:
        try:
            global cnx
            global cursor
            
            cnx = mysql.connector.connect(**db_config3)
            cursor = cnx.cursor()
            return
        except mysql.connector.Error as err:
            
            print("Database-Connection failed, Error: ", err)
            
            print("Datenbank Verbindungsversuche : {}".format(connection_counter))
            connection_counter += 1
            sleep(5)    


# Datenbankabfrage
def get_input():
    global query_input
    global Input
    global Device
    global Controlmode
    global StartStopSignal
    global Throttleposition
    global cnx
    global cursor
    
    if cnx.is_connected():
        try:
            cursor.execute(query_input)
            Input = cursor.fetchall()
            Input = Input[0]
            Device = Input[0]
            Controlmode = Input[1]
            StartStopSignal = Input[2]
            Throttleposition = Input[3]
        except mysql.connector.Error as err:
            print("Connection lost")
            print(err)
            cursor.close()
            cnx.close()
            db_connection()
    else:
        print("Connection lost")
        cursor.close()
        cnx.close()
        db_connection()           
    
        
    
#Datenbank aktualisieren
def update_output(update, value):
    global cnx
    global cursor
    
    if cnx.is_connected():
        try:
            cursor.execute(update % value)
            cnx.commit()
        except:
            print("Connection lost")
            cursor.close()
            cnx.close()
            db_connection()
            update_output(update, value)
    else:
        print("Connection lost")
        cursor.close()
        cnx.close()
        db_connection()
        update_output(update, value)

def update_output_all():
    global cnx
    global cursor
    global update_output_table
    global Zustand
    global Connection_Counter
    global Motor_an_Flag
    global Not_Aus_Flag
    
    if cnx.is_connected():
        try:
            cursor.execute(update_output_table.format(Connection_Counter, Motor_an_Flag, Zustand.value, frequence_Reader.RPM, Not_Aus_Flag))
            cnx.commit()
        except:
            print("Connection lost")
            cursor.close()
            cnx.close()
            db_connection()
    else:
        print("Connection lost")
        cursor.close()
        cnx.close()
        db_connection()



def Motor_start():
    #Led anschalten oder so
    sleep(2)


    
def LED_off():
    global LED_blue_GPIO


    # Nullsetzen der LED Ausgnänge
    pi.write(LED_blue_GPIO, 0)

    

    
def LED_starting():
    global LED_blue_GPIO
    
    pi.write(LED_blue_GPIO, 1)
    
    
def LED_motor_an():
    global LED_blue_GPIO
 
    pi.write(LED_blue_GPIO, 0)

    
#gpio Zuweisung
pi = pigpio.pi()    

# Pinzuweisung(in GPIO)
# Ausgänge
# PWM
Gas_GPIO = 14
Chokehebel_fahren_GPIO = 15
Chokehebel_drehen_GPIO = 18

#LED
LED_blue_GPIO = 8


# Relais
Gas_Relais_GPIO = 23
Chokehebel_fahren_Relais_GPIO = 24
Chokehebel_drehen_Relais_GPIO = 25

#Eingänge
Not_Aus_GPIO = 17
Frequenz_GPIO = 20 #normal 27, umgesteckt für Q1 Ausgang


# Angefahrene Winkel der Servos deklarieren, bei Werkzeugwechsel anpassen

Winkel_Chokehebel_einfahren = 2
Winkel_Chokehebel_ausfahren = 30
Winkel_Chokehebel_aus = 58
Winkel_Chokehebel_Betrieb = 19
Winkel_Chokehebel_Warmstart = -8
Winkel_Chokehebel_Kaltstart = -28
Winkel_Gas_min = -26
Winkel_Gas_Anschlag = -19
Winkel_Gas_max = 5

# Servos deklarieren (Pin, Nullstellung, min Winkel, max Winkel)

Gas_Servo = Servo(pi, Gas_GPIO,1500, Winkel_Gas_min, Winkel_Gas_Anschlag, Winkel_Gas_max)
Chokehebel_fahren_Servo = Servo(pi, Chokehebel_fahren_GPIO, 1500)
Chokehebel_drehen_Servo = Servo(pi, Chokehebel_drehen_GPIO, 1500)

# Frequenz Thread definieren

frequence_Reader = frequence_Thread(pi, Frequenz_GPIO, 2)

# Not Aus Klasse deklarieren

Not_Aus = Not_Aus_class(pi, Not_Aus_GPIO)

# Zustand deklarieren

Zustand = Zustaende.Aus

#Ausgänge deklarieren
#Relais
pi.set_mode(Gas_Relais_GPIO, pigpio.OUTPUT)
pi.set_mode(Chokehebel_fahren_Relais_GPIO, pigpio.OUTPUT)
pi.set_mode(Chokehebel_drehen_Relais_GPIO, pigpio.OUTPUT)
# Pull Down der Relaisausgänge
pi.set_pull_up_down(Gas_Relais_GPIO, pigpio.PUD_DOWN)
pi.set_pull_up_down(Chokehebel_fahren_Relais_GPIO, pigpio.PUD_DOWN)
pi.set_pull_up_down(Chokehebel_drehen_Relais_GPIO, pigpio.PUD_DOWN)

#Nullsetzen der Relaisausgänge
pi.write(Gas_Relais_GPIO, 0)
pi.write(Chokehebel_fahren_Relais_GPIO, 0)
pi.write(Chokehebel_drehen_Relais_GPIO, 0)

#LEDs
pi.set_mode(LED_blue_GPIO, pigpio.OUTPUT)


# Pull Down der LEDausgänge
pi.set_pull_up_down(LED_blue_GPIO, pigpio.PUD_DOWN)


# Nullsetzen der LED Ausgnänge
pi.write(LED_blue_GPIO, 0)


# Flags

Kaltstart_Flag = False
Warmstart_Flag = False
Betrieb_Flag = False
ChangeMode_Flag = False
Motor_an_Flag = False
Not_Aus_Flag = False

# Datenbankkonfiguration

# Munirahs DB

db_config1 = { 'user': 'sql7291661',
               'password' : '5NMuDuvLTZ',
               'host' : 'sql7.freemysqlhosting.net',
               'port' : '3306',
               'database' : 'sql7291661',
               'connect_timeout' : 5}

# Renes DB--> mit endgültiger Struktur

db_config2 = { 'user': 'sql2295094',
               'password' : 'jJ8!xI1%',
               'host' : 'sql2.freemysqlhosting.net',
               'port' : '3306',
               'database' : 'sql2295094'}

#Daniels DB
db_config3 = { 'user': 'VisiuLdKXI',
               'password' : 'fdakQ9qTvL',
               'host' : 'remotemysql.com',
               'port' : '3306',
               'database' : 'VisiuLdKXI',
               'connect_timeout' : 5}

# Befehle für Datenbank request und write

query_input = "SELECT * from input"
update_Connection = "UPDATE output SET Statusconnection = %s"
update_Statusengine = "UPDATE output SET Statusengine = %s"
update_Startcounter = "UPDATE output SET Startcounter = %s"
update_mode = "UPDATE output SET StatusMode = %s"
update_RPM = "UPDATE output SET rpm = %s"
update_Not_Aus = "UPDATE output SET lokalEmergency = %s"

update_output_table = "UPDATE output SET Statusconnection = {}, Statusengine = {}, StatusMode = {}, rpm ={}, lokalEmergency = {}"

# Variabeln für Datenbankabfragen
#Input
Input = None
Device = None
Controlmode = None
StartStopSignal = None
Throttleposition = None
connection_counter = 0


#Output

Connection_Counter = 0
Counter = 0


# Zeit
Motor_Timer = time()
Connection_Timer = 0

# Sonstige Variablen



if __name__ == "__main__":
    frequence_Reader.start()
    db_connection()
    Relais_Setup()
    Grundstellung()
    
    
    try:
        while True:
            get_input()
            
            # Connection Scheduler
            if Connection_Timer + 0.2 < time():
                Connection_Counter += 1
                update_output_all()
                #print("Connection updatet")
                print(frequence_Reader.averagefrequence,"\t", frequence_Reader.RPM)
                Connection_Timer = time()

            
            if Device == "MS" and not Not_Aus_Flag:
                # Warm oder Kaltstart
                if not ChangeMode_Flag and Controlmode == 0 and not Kaltstart_Flag and StartStopSignal == 0 and not Not_Aus_Flag and not Motor_an_Flag:
                    ChangeMode_Flag = True
                    Kaltstart = Kaltstart_Thread()
                    Kaltstart.start()
                    Zustand = Zustaende.Kaltstart

                elif not ChangeMode_Flag and Controlmode == 1 and not Warmstart_Flag and StartStopSignal == 0 and not Not_Aus_Flag and not Motor_an_Flag:
                    ChangeMode_Flag = True
                    Warmstart = Warmstart_Thread()
                    Warmstart.start()
                    Zustand = Zustaende.Warmstart

                elif not ChangeMode_Flag and Controlmode == 3 and not Betrieb_Flag and StartStopSignal == 0 and not Not_Aus_Flag and not Motor_an_Flag:
                    ChangeMode_Flag = True
                    Betrieb = Betrieb_Thread()
                    Betrieb.start()
                    Zustand = Zustaende.Betrieb

                    
                # Motor starten       
                if (Kaltstart_Flag or Warmstart_Flag or Betrieb_Flag) and StartStopSignal == 1 and not Motor_an_Flag and not Not_Aus_Flag and not ChangeMode_Flag:
                    if Counter == 0:
                         LED_starting()
            
                    if Motor_Timer + 10 < time():
                        LED_off()
                        if frequence_Reader.RPM > 1500:
                            print("Motor an erkannt")
                            Motor_an_Flag = True
                            LED_motor_an()
                            if Warmstart_Flag or Kaltstart_Flag:
                                Betrieb = Betrieb_Thread()
                                Betrieb.start()
                                Zustand = Zustaende.Betrieb
                            continue
                        
                        # Bei 5 Startversuchen in Warm oder Kaltstart auf Betrieb umschalten 
                        if Counter == 5 and (Kaltstart_Flag or Warmstart_Flag) and StartStopSignal == 1 and not Motor_an_Flag and not Not_Aus_Flag and not ChangeMode_Flag:
                            ChangeMode_Flag = True
                            print("Fünf Startversuche in Warm/Kaltstart, umstellen auf Betrieb")
                            Betrieb = Betrieb_Thread()
                            Betrieb.start()
                            Zustand = Zustaende.Betrieb
                            continue
                    
                    if Motor_Timer + 15 < time():
                        LED_starting()
                        Counter += 1
                        Motor_Timer = time()
                        print("Motor Start\n Anzahl Startversuche: {}".format(Counter))
                        
                elif StartStopSignal == 0:
                    Counter = 0
                
 
                 # Gassteuerung aktivieren
                if (Kaltstart_Flag or Warmstart_Flag or Betrieb_Flag) and Motor_an_Flag and Gas_Servo.Prozent != Throttleposition and not Not_Aus_Flag:
                    print("aktuelles Gas in Prozent: ", Throttleposition)
                    Gas_Servo.gas_prozent(Throttleposition)
                
                #Motor ausschalten
                if Motor_an_Flag and (StartStopSignal == 0 or frequence_Reader.RPM == 0) and not Not_Aus_Flag:
                    print("Motor war an, ausstellen")
                    ChangeMode_Flag = True
                    Motor_an_Flag = False
                    LED_off()
                    Counter = 0
                    Motor_stopp = Motor_stopp_Thread()
                    Motor_stopp.start()
                    Zustand = Zustaende.Aus


                    

    except KeyboardInterrupt:
        print("Anlage aus")
        Gas_Servo.ausschalten()
        Chokehebel_fahren_Servo.ausschalten()
        Chokehebel_drehen_Servo.ausschalten()
        pi.write(Gas_Relais_GPIO, 0)
        pi.write(Chokehebel_fahren_Relais_GPIO, 0)
        pi.write(Chokehebel_drehen_Relais_GPIO, 0)
        pi.stop()
        Not_Aus.cancel()
        if cnx.is_connected():
            cursor.close()
            cnx.close()
        
        
        
 