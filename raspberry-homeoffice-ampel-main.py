# -*- coding: utf-8 -*-
#-----------------------------
#
#   MQTT-homeoffice light
#
#   by: Marvin Schmid
#
#   version: 1.5
#
#-----------------------------
try:
    from sys import exit
except ImportError:
    print("Die Bibliothek: sys konnte nicht geladen werden")
try:
    import time
except ImportError:
    exit("Die Bibliothek: time konnte nicht geladen werden")
try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("Die Bibliothek: paho MQTT konnte nicht geladen werden")
try:
    from termcolor import colored, cprint
except ImportError:
    exit("Die Bibliothek: termcolor konnte nicht geladen werden")
try:
    import math
except ImportError:
    print("Die Bibliothek: math konnte nicht geladen werden")
try:
    import logging
except ImportError:
    exit("Die Bibliothek: logging konnte nicht geladen werden")
try:
    import blinkt
except ImportError:
    exit("Die Bibliothek: blinkt konnte nicht geladen werden")
try:
    import configparser
except ImportError:
    exit("Die Bibliothek: configparse konnte nicht geladen werden")
try:
    import signalleuchte
except ImportError:
    exit("Die Bibliothek: signalleuchte konnte nicht geladen werden")


#Textbeispiele
TEXT_START = colored('  program started', 'green', attrs=['bold'])
TEXT_OK = colored('OK', 'green', attrs=['bold'])
TEXT_FALSCHE_FORMATIERUNG = colored('Fehler: Falsch formatierter Befehl', 'red')
TEXT_ENDE = colored('  Das Programm wurde durch den Benutzer beendet', 'green', attrs=['bold'])
TEXT_FEHLER = colored('WARN', 'red', attrs=['bold', 'reverse'])
print(time.strftime("%d.%m.%Y %H:%M:%S") + TEXT_START + "\n")

#Load Config file
try:
    config = configparser.ConfigParser()                                     
    config.read('config.ini')
except:
    exit("config konnte nicht geladen werden")

#Logging
try:
    logging.basicConfig(filename=config.get('LOGS','FILENAME'), format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.info('Logging app started')
except:
    exit(time.strftime("%d.%m.%Y %H:%M:%S  ") + TEXT_FEHLER +  "  Probleme Beim Logging: Log konnte nicht erstellt werden")

#MQTT Einstellungen

MQTT_SERVER = config.get('MQTT','SERVER')
MQTT_PATH = config.get('MQTT','PATH')
MQTT_CLIENT_NAME = config.get('MQTT','CLIENT_NAME')
MQTT_CLIENT_USERNAME = config.get('MQTT','CLIENT_USERNAME')
MQTT_CLIENT_PW = config.get('MQTT','CLIENT_PASSWORD')
MQTT_PORT = config.get('MQTT','PORT')
MQTT_BROKER = config.get('MQTT','BROKER')
MQTT_TOPIC = config.get('MQTT', 'TOPIC')
CLEAN_SESSION=True


def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   #print("subscribed with qos",granted_qos, "\n")
   time.sleep(1)
   logging.info("sub acknowledge message id="+str(mid))
   pass

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    global command
    command = msg
    logging.info(str("message received: ", msg))
    logging.info(str("message topic: ", message.topic))
    pass

def on_disconnect(client, userdata,rc=0):
    logging.info("DisConnected result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    logging.info("Connected flags"+str(flags)+"result code "+str(rc))


client= mqtt.Client(MQTT_CLIENT_NAME,False)       #create client object
client.username_pw_set(MQTT_CLIENT_USERNAME, MQTT_CLIENT_PW)
client.on_subscribe = on_subscribe   #assign function to callback
client.on_disconnect = on_disconnect #assign function to callback
client.on_connect = on_connect #assign function to callback
client.on_message=on_message
client.connect(MQTT_BROKER,MQTT_PORT, keepalive=60)           #establish connection
time.sleep(1)
client.loop_start()
client.subscribe(MQTT_TOPIC)       #need to be chanched to the individual server
print("Connected to MQTT Broker: " + MQTT_BROKER)


#important variable 
command = 0

print(time.strftime("%d.%m.%Y %H:%M:%S") + "  Log Funktion" + "   [ " + TEXT_OK + " ]")
print(time.strftime("%d.%m.%Y %H:%M:%S") + "  Connected to MQTT Broker: " + MQTT_BROKER + "   [ " + TEXT_OK + " ]")

try:
    while True:
        command = int(command)
        if (command == 0):
            signalleuchte.clear()
        elif (command == 1):
            signalleuchte.solid_red()
        elif (command == 2):
            signalleuchte.solid_green()
        elif (command == 3):
            signalleuchte.solid_blue()
        elif (command == 4):
            signalleuchte.solid_orange()
        elif (command == 5):
            signalleuchte.solid_green_light()
        elif (command == 6):
            signalleuchte.larson_hue()
        elif (command == 7):
            signalleuchte.larson()
        elif (command == 8):
            signalleuchte.rainbow()
        elif (command == 9):
            signalleuchte.binary_clock()
        elif (command == 10):
            signalleuchte.solid_white()
        elif (command == 11):
            signalleuchte.pulse_blue()
        elif (command == 12):
            signalleuchte.pulse_red()
        elif (command == 13):
            signalleuchte.morse_code()
        elif (command == 14):
            signalleuchte.dash_red()
        elif (command == 15):
            signalleuchte.dot_blue()
        else:
            print('Unbekanntes Kommando')
except KeyboardInterrupt:
    logging.warning("Programm beendet")
    client.disconnect()
    client.loop_stop()
    print("\n")
    print("-------------------------------")
    print("Programm wurde beendet")
