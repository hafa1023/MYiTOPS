# MYiTOPS - Workshop: Remote Control via Cyber-physical Systems
Implementation of "International Team Oriented Project Studies" in the field of cyberphysical systems in German - Malaysian tandems in Germany and Malaysia in mechatronics and vehicle technology.

## Set up Remote Control System

Before you can use the software offered here, you have to prepare the Raspberry Pi and the Windows-Server (computer) with LabVIEW. 

### Prerequisites
#### Rasberry Pi 3
 * [Download the latest version of Rasbian](https://www.raspberrypi.org/downloads/raspbian/). Follow the instructions on the page to get your RPI 3 up and running. Best is to use the desktop version. 

 * Starting with your RPI 3 and a new Rasbian operating system, the following external Python modules are to be installed. Open a terminal window (LXTerminal, a black monitor icon in the menu) and enter the following:

```
 sudo apt update
 sudo apt install python3-pyside
 
 ```
 
 #### LabVIEW
* To use the software, NI LabVIEW version 2015 or later is required. LabVIEW is a development environment and is for any measurement or control system. If you don't have a license for the development environment, you can use the evaluating version for now. [You can download it here](http://www.ni.com/de-de/shop/labview.html). 
* SQLite is used here for the database. The SQLite library can be integrated directly into corresponding applications so that no additional server software is required. Here the SQLite library for LabVIEW by Dr. James Powell was used. [Here you can download and install it](http://sine.ni.com/nips/cds/view/p/lang/de/nid/212894). 

#### Soldering from RPI-Demo-Breadboard
Follow this [schema](https://github.com/IKKUengine/MYiTOPS/blob/master/breadboard_RPI_MYiTOPS.pdf)! Required parts are listed on the circuit diagram.

## Deployment and Starting
If so far everything is installed, then clone or download [Project-Folder](https://github.com/IKKUengine/MYiTOPS/archive/master.zip) to your home directory of your Raspberry Pi and Windows-Computer. Next download also the ηNet-server to your Windows computer: [ηNet-Server](https://github.com/IKKUengine/ThreadedQtEtaNetServer/blob/master/bin/EtaNetServerV0_9_4.zip).
### On the Windows-PC
#### ηNet-Server
* Connect your PC with etaNet-Router-Wlan-Network
* Unzip the .zip file and double-click on the etanet.exe. Accept all windows safety regulations...
* Chose an Interface IP, that the etaNet-Router gave you and let the port 50005.

The system is programmed so that the corresponding database and its structure is created automatically at startup. You can also use the [DB Browser for SQLite](https://sqlitebrowser.org/). you can find the .db-file in the same directory as the .exe-file of the server.

#### LabVIEW App
Navigate to "Software" (MYiTOPS project folder) on Windows-PC and look for your LabVIEW version and find the file with the extension .lvproj and double-click it. 
A project explorer will be open. Double-click CBSControlling.vi. A window with a user interface will open. At the top left is an icon with an arrow pointing to the right (run button). Please press this button. The application wants you to navigate to the .db file and set it. Follow the instructions...

### On your RPI
If you have started your RPI (with Rasbian OS), you will find a raspberry icon at the top right. The icon takes you to the main menu. Navigate to Programming-> Thonny. Thonny is an integrated development environment for Python. Navigate to "Software" (MYiTOPS project folder) on RPI and look for Python3-Folder and RPIClient_DemoBoard.py. Look into the code. On one position please enter the IP address of the server here. Change the transfer rate if desired.

'''
ipAdress = '192.168.178.XX'

TRANSFERRATE = 0.2
'''
and search for this line of code and change the name as desired:
'''
 header = "'MYiTOPS-RPI-Client 3'
'''

At the top left of Thonny IDE is an icon with an play button (run button), klick on it. When your client name appears in the LabVIEW application and you can control the demo board, everything worked fine.


