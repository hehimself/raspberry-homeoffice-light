# -*- coding: utf-8 -*-
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
    import colorsys
except ImportError:
    exit("Die Bibliothek: colorsys konnte nicht geladen werden")
try:
    import math
except ImportError:
    print("Die Bibliothek: math konnte nicht geladen werden")
try:
    import numpy
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")
try:
    import logging
except ImportError:
    exit("Die Bibliothek: logging konnte nicht geladen werden")
try:
    import unicornhat as unicorn
except ImportError:
    exit("Die Bibliothek: Unicorn konnte nicht geladen werden")
try:
    from random import randint
except ImportError:
    exit("Die Bibliothek: Random konnte nicht geladen werden")

#Textbeispiele
text_start = colored('  Programm wurde gestartet', 'green', attrs=['bold'])
text_ok = colored('OK', 'green', attrs=['bold'])
text_falsche_formatierung = colored('Fehler: Falsch formatierter Befehl', 'red')
text_ende = colored('  Das Programm wurde durch den Benutzer beendet', 'green', attrs=['bold'])
text_fehler = colored('WARN', 'red', attrs=['bold', 'reverse'])
print(time.strftime("%d.%m.%Y %H:%M:%S") + text_start + "\n")

#ASCII Beispiel
ASCIIPIC = [
     "  X  X  "
    ,"        "
    ,"X      X"
    ," XXXXXX "
    ,"        "
    ,"        "
    ,"        "
    ]

#Logging
try:
    logging.basicConfig(filename='Signalleuchte_07.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.info('Logging app started')
except:
    exit(time.strftime("%d.%m.%Y %H:%M:%S  ") + text_fehler +  "  Probleme Beim Logging: Log konnte nicht erstellt werden")

#Unicorn Einstellungen
try:
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
    width,height=unicorn.get_shape()
except:
    logging.error('Einstellungen zum Unicronhat konten nicht vorgenommen werden')
    exit(time.strftime("%d.%m.%Y %H:%M:%S  ") + text_fehler + "  Einstellungen zum Unicornhat konnten nicht vorgenommen werden")

if height==width:
    delta=0
else:
    delta=2

#nötig für Alarm Animation
def make_gaussian(fwhm):
    x = numpy.arange(0, 8, 1, float)
    y = x[:, numpy.newaxis]
    x0, y0 = 3.5, 3.5
    fwhm = fwhm
    gauss = numpy.exp(-4 * numpy.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

#Alarm Animation
def alarm():
    for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
        fwhm = 5.0/z
        gauss = make_gaussian(fwhm)
        start = time.time()
        for y in range(height):
            for x in range(width):
                h = 1.0/(x + y + delta + 1)
                s = 0.8
                if height<=width:
                    v = gauss[x,y+delta]
                else:
                    v = gauss[x+delta,y]
                rgb = colorsys.hsv_to_rgb(h, s, v)
                r = int(rgb[0]*255.0)
                g = int(rgb[1]*255.0)
                b = int(rgb[2]*255.0)
                unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
        end = time.time()
        t = end - start
        if t < 0.04:
            time.sleep(0.04 - t)

#Roter Alarm Animation
def alarm_rot():
    unicorn.brightness(1)
    for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
        fwhm = 5.0/z
        gauss = make_gaussian(fwhm)
        start = time.time()
        for y in range(height):
            for x in range(width):
                h = 1.0/(x + y + delta + 1)
                s = 0.8
                if height<=width:
                    v = gauss[x,y+delta]
                else:
                    v = gauss[x+delta,y]
                rgb = colorsys.hsv_to_rgb(h, s, v)
                r = int(rgb[0]*255.0)
                g = int(rgb[1]*0.0)
                b = int(rgb[2]*0.0)
                unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
        end = time.time()
        t = end - start
        if t < 0.04:
            time.sleep(0.04 - t)
    unicorn.brightness(0.5)

#Regenbogen Animation
def rainbow():
    spacing = 360.0 / 16.0
    hue = 0
    for i in xrange(0,2):
        hue = int(time.time() * 100) % 360
        for x in range(8):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            for y in range(4):
                unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
        time.sleep(0.05)

#Regenbogen Animation
def rainbow_2():
    i = 0.0
    offset = 30
    for t in xrange(0,100):
        i = i + 0.3
        for y in range(height):
                for x in range(width):
                        r = 0
                        g = 0
                        r = (math.cos((x+i)/2.0) + math.cos((y+i)/2.0)) * 64.0 + 128.0
                        g = (math.sin((x+i)/1.5) + math.sin((y+i)/2.0)) * 64.0 + 128.0
                        b = (math.sin((x+i)/2.0) + math.cos((y+i)/1.5)) * 64.0 + 128.0
                        r = max(0, min(255, r + offset))
                        g = max(0, min(255, g + offset))
                        b = max(0, min(255, b + offset))
                        unicorn.set_pixel(x,y,int(r),int(g),int(b))
        unicorn.show()
        time.sleep(0.01)
        t += 1

#Random Sparkels
def random_sparkels():
    for i in xrange(0,10):
        x = randint(0, (width-1))
        y = randint(0, (height-1))
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
        time.sleep(0.001)

#ASCII PIC
t = -1
def ascii_pic():
    for i in xrange(0,5):
        global t
        i = t
        i = 0 if i>=100*len(ASCIIPIC) else i+1 # avoid overflow
        for h in range(height):
            for w in range(width):
                hPos = (i+h) % len(ASCIIPIC)
                chr = ASCIIPIC[hPos][w]
                if chr == ' ':
                    unicorn.set_pixel(w, h, 0, 0, 0)
                else:
                    unicorn.set_pixel(w, h, 255, 0, 0)
        unicorn.show()
        time.sleep(0.2)

#cross
points = []
class cross:
    def __init__(self):

        self.direction = randint(1, 4)
        if self.direction == 1:
            self.x = randint(0, width - 1)
            self.y = 0
        elif self.direction == 2:
            self.x = 0
            self.y = randint(0, height - 1)
        elif self.direction == 3:
            self.x = randint(0, width - 1)
            self.y = height - 1
        else:
            self.x = width - 1
            self.y = randint(0, height - 1)

        self.colour = []
        for i in range(0, 3):
            self.colour.append(randint(100, 255))
def update_positions():
    for point in points:
        if point.direction == 1:
            point.y += 1
            if point.y > height - 1:
                points.remove(point)
        elif point.direction == 2:
            point.x += 1
            if point.x > width - 1:
                points.remove(point)
        elif point.direction == 3:
            point.y -= 1
            if point.y < 0:
                points.remove(point)
        else:
            point.x -= 1
            if point.x < 0:
                points.remove(point)
def plot_points():
    unicorn.clear()
    for point in points:
        unicorn.set_pixel(point.x, point.y, point.colour[0], point.colour[1], point.colour[2])
    unicorn.show()
def cross_animation():
    if len(points) < 10 and randint(0, 5) > 1:
        points.append(cross())
    plot_points()
    update_positions()
    time.sleep(0.03)

#snow
rows = []
row_pointer = 0
def init():

    # create a buffer of <height> blank rows
    for i in range(height):
        rows.append(get_blank_row())
def get_blank_row():

    # generate a blank row
    return [0] * width
def get_new_row():

    # get a new blank row and add a random brightness snowflake to a random column
    row = get_blank_row()
    row[randint(0, width - 1)] = 50 + randint(0, 155)
    return row
def update_display():

    # keep track of the row we are updating
    c = row_pointer
    for h in range(height):
        for w in range(width):
            # val is between 50 and 255
            val = rows[c][w]

            # invert coordinates
            unicorn.set_pixel((width - 1) - w, (height - 1) - h, val, val, val)
        c += 1
        if c > height - 1:
            c = 0
    unicorn.show()
def step():
    global row_pointer

    # add new row at current row pointer
    # leave other rows the same, display will start from this one which overwrites the
    # oldest existing row from the last time we updated the display
    rows[row_pointer] = get_new_row()
    update_display()

    # determine next row pointer, wrapping around if we went past zero
    row_pointer -= 1
    if row_pointer < 0:
        row_pointer = height - 1
def snow():
    step()
    time.sleep(0.3)
init()

#Alarm 2
def alarm_rot_2():
    unicorn.set_all(255, 0, 0)
    unicorn.show()
    time.sleep(1)
    unicorn.clear()
    unicorn.show()
    time.sleep(1)

def alarm_rot_3():
    x = 0
    y = 255
    for i in range(510):
        if x <= 255:
            unicorn.set_all(0,x,0)
            unicorn.show()
            x = x + 1
        if x >= 255:
            unicorn.set_all(0,y,0)
            unicorn.show()
            y = y - 1
        time.sleep(0.001)
    time.sleep(3)

#MQTT Kommunikation
CLEAN_SESSION=True
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    global command
    command = msg
    logging.info(str("message received: ", msg))
    logging.info(str("message topic: ", message.topic))

def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print(time.strftime("%d.%m.%Y %H:%M:%S") + "  Connection"+ "   [ " + text_ok + " ]")
    elif(rc == 1):
        print(time.strftime("%d.%m.%Y %H:%M:%S") + text_fehler + "  Verbindung abgelehnt Grund: nicht akzeptierte Protokollversion")
        logging.error('MQTT Verbindung wurde abgelehnt Grund: nicht akzeptierte Protokollversion')
    elif(rc == 2):
        print(time.strftime("%d.%m.%Y %H:%M:%S") + text_fehler + "  Verbindung abgelehnt Grund: identifier rejected")
        logging.error('MQTT Verbindung wurde abgelehnt Grund: identifier rejected')
    elif(rc == 3):
        print(time.strftime("%d.%m.%Y %H:%M:%S") + text_fehler + "  Verbindung abgelehnt Grund: Server nicht erreichbar")
        logging.error('MQTT Verbindung wurde abgelehnt Grund: Server nicht erreichbar')
    elif(rc == 4):
        print(time.strftime("%d.%m.%Y %H:%M:%S") + text_fehler + "  Verbindung abgelehnt Grund: falscher Benutzername oder Passwort")
        logging.error('MQTT Verbindung wurde abgelehnt Grund: falscher Benutzername oder Passwort')
    elif(rc == 5):
        print(time.strftime("%d.%m.%Y %H:%M:%S") + text_fehler + "  Verbindung abgelehnt Grund: Keine Autorisierung")
        logging.error('MQTT Verbindung wurde abgelehnt Grund: Keine Autorisierung')
    else:
        logging.critical('MQTT Verbindung wurde abgelehnt Grund: Kein Grund bekannt')
        exit(time.strftime("%d.%m.%Y %H:%M:%S") + text_fehler + "  Verbindung abgelehnt Grund: Kein Grund bekannt")

def on_disconnect(client, userdata,rc=0):
    logging.info("DisConnected result code "+str(rc))
    if rc != 0:
        print("unexpected disconnect")

def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   #print("subscribed with qos",granted_qos, "\n")
   time.sleep(1)
   logging.info("sub acknowledge message id="+str(mid))
   pass

BROKER_ADDRESS = "iobrokerpi"

client = mqtt.Client("Signalleuchte",False)
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message


client.username_pw_set("mqtt2","g8b7oUbT")
client.connect(BROKER_ADDRESS, port=8692)
time.sleep(1)
print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_start()
client.subscribe("house/client_a")

#WICHTIGE Variable
command = 0

print(time.strftime("%d.%m.%Y %H:%M:%S") + "  Log Funktion" + "   [ " + text_ok + " ]")
print(time.strftime("%d.%m.%Y %H:%M:%S") + "  Connected to MQTT Broker: " + BROKER_ADDRESS + "   [ " + text_ok + " ]")
try:
    while True:
        command = int(command)
        if (command == 0):
            unicorn.clear()
            unicorn.show()
            time.sleep(0.5)
        elif (command == 1):
            alarm()
        elif (command == 2):
            alarm_rot()
        elif (command == 3):
            rainbow()
        elif (command == 4):
            rainbow_2()
        elif (command == 5):
            random_sparkels()
        elif (command == 6):
            ascii_pic()
        elif (command == 7):
            cross_animation()
        elif (command == 8):
            snow()
        elif (command == 9):
            alarm_rot_2()
        elif (command == 10):
            alarm_rot_3()
        else:
            print('Unbekanntes Kommando')

except KeyboardInterrupt:
    logging.info('Der Butzer hat das Programm beendet')
    client.disconnect()
    client.loop_stop()
    print("\n")
    print(time.strftime("%d.%m.%Y %H:%M:%S") + text_ende)
    print("\n")