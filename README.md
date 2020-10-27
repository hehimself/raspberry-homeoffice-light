# Raspberry Pi Homeoffice Ampel [MQTT]
[![Generic badge](https://img.shields.io/badge/Status-WIP-green.svg)](https://shields.io/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

 Raspberry pi Ampel zum anzeigen, ob man sich gerade in einer Videokonferenz befindet und nicht gestört werden will


Die Hauptfunktionen der Ampel sind die Farben:
* Grün (man kann gestört werden)
* Gelb (bitte klopfen)
* Rot  (bitte nicht stören)

## Usage:

## Installation:

## Funktionen
Die LED Leiste "Blink" von Pimoroni wird über die blinkt Biblothek angesteuert. Um die LED Leitste auszuschalten wird folgende Funktion benutzt:
```python
def clear():
    blinkt.clear()
    blinkt.show()
    time.sleep(0.5)
```
Die Hauptfunktionen der Ampel: (weitere Animationen sind in [signalleuchte.py](https://github.com/hehimself/raspberry-homeoffice-light/blob/main/signalleuchte.py) verfügbar)
```python
def solid_red():
    blinkt.set_all(255,0,0)
    blinkt.show()
    
def solid_green():
    blinkt.set_all(0,255,0)
    blinkt.show()    

def solid_orange():
    blinkt.set_all(255,128,0)
    blinkt.show()
```

So kann man immer anzeigen, dass man gerade nicht gestört werden will:
![Farmers Market Finder Demo](photos/video_red.gif)
