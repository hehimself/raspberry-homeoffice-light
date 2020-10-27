#!/usr/bin/python
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
    import blinkt
except ImportError:
    exit("Die Bibliothek: blinkt konnte nicht geladen werden")

    
#------------Animationsbereich------------
#Variablen für Animation: larson_hue
FALLOFF = 1.9
SCAN_SPEED = 4
blinkt.set_clear_on_exit()
start_time = time.time()

#Variablen für Animation: larson
blinkt.set_clear_on_exit()
REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]
start_time = time.time()

#Variablen für Animation: rainbow
spacing = 360.0 / 16.0
hue = 0
blinkt.set_clear_on_exit()

def make_gaussian(fwhm):
    x = numpy.arange(0, blinkt.NUM_PIXELS, 1, float)
    y = x[:, numpy.newaxis]
    x0, y0 = 3.5, 3.5
    fwhm = fwhm
    gauss = numpy.exp(-4 * numpy.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

def pulse_blue():
    for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
        fwhm = 5.0/z
        gauss = make_gaussian(fwhm)
        start = time.time()
        y = 4
        for x in range(blinkt.NUM_PIXELS):
            h = 0.5
            s = 1.0
            v = gauss[x, y]
            rgb = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = [int(255.0 * i) for i in rgb]
            blinkt.set_pixel(x, r, g, b)
        blinkt.show()
        end = time.time()
        t = end - start
        if t < 0.04:
            time.sleep(0.04 - t)

def pulse_red():
    for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
        fwhm = 5.0/z
        gauss = make_gaussian(fwhm)
        start = time.time()
        y = 4
        for x in range(blinkt.NUM_PIXELS):
            h = 0
            s = 1.0
            v = gauss[x, y]
            rgb = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = [int(255.0 * i) for i in rgb]
            blinkt.set_pixel(x, r, g, b)
        blinkt.show()
        end = time.time()
        t = end - start
        if t < 0.04:
            time.sleep(0.04 - t)

def larson_hue():
    delta = (time.time() - start_time)
    # Offset is a sine wave derived from the time delta
    # we use this to animate both the hue and larson scan
    # so they are kept in sync with each other
    offset = (math.sin(delta * SCAN_SPEED) + 1) / 2

    # Use offset to pick the right colour from the hue wheel
    hue = int(round(offset * 360))

    # Maximum number basex on NUM_PIXELS
    max_val = blinkt.NUM_PIXELS - 1

    # Now we generate a value from 0 to max_val
    offset = int(round(offset * max_val))

    for x in range(blinkt.NUM_PIXELS):
        sat = 1.0

        val = max_val - (abs(offset - x) * FALLOFF)
        val /= float(max_val) # Convert to 0.0 to 1.0
        val = max(val,0.0) # Ditch negative values

        xhue = hue # Grab hue for this pixel
        xhue += (1-val) * 10 # Use the val offset to give a slight colour trail variation
        xhue %= 360 # Clamp to 0-359
        xhue /= 360.0 # Convert to 0.0 to 1.0

        r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(xhue, sat, val)]

        blinkt.set_pixel(x, r, g, b, val / 4)

    blinkt.show()

    time.sleep(0.001)

def larson():
    # Sine wave, spends a little longer at min/max
    # delta = (time.time() - start_time) * 8
    # offset = int(round(((math.sin(delta) + 1) / 2) * (blinkt.NUM_PIXELS - 1)))
    # Triangle wave, a snappy ping-pong effect
    delta = (time.time() - start_time) * 16
    offset = int(abs((delta % len(REDS)) - blinkt.NUM_PIXELS))
    for i in range(blinkt.NUM_PIXELS):
        blinkt.set_pixel(i , REDS[offset + i], 0, 0)
    blinkt.show()
    time.sleep(0.01)

def rainbow():
    blinkt.set_brightness(0.2)
    hue = int(time.time() * 100) % 360
    for x in range(blinkt.NUM_PIXELS):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        blinkt.set_pixel(x, r, g, b)

    blinkt.show()
    time.sleep(0.001)

def binary_clock():
    #Variablen für Animation: binary_clock
    blinkt.set_clear_on_exit()
    MODE_HOUR = 0
    MODE_MIN = 1
    MODE_SEC = 2
    time_to_stay_in_mode = 3
    time_in_mode = 0
    mode = 0
    lh = 0
    lm = 0
    t = time.localtime()
    h, m, s = t.tm_hour, t.tm_min, t.tm_sec

    if h != lh:
        mode = MODE_HOUR
        time_in_mode = 0

    elif m != lm:
        mode = MODE_MIN
        time_in_mode = 0

    lm = m
    lh = h

    blinkt.clear()

    if (s % 2) == 0:
        blinkt.set_pixel(1, 64, 64, 64)

    if mode == MODE_HOUR:
        blinkt.set_pixel(0, 255, 0, 0)
        for x in range(6):
            bit = (h & (1 << x)) > 0
            r, g, b = [128 * bit] * 3
            blinkt.set_pixel(7 - x, r, g, b)

    if mode == MODE_MIN:
        blinkt.set_pixel(0, 0, 255, 0)
        for x in range(6):
            bit = (m & (1 << x)) > 0
            r, g, b = [128 * bit] * 3
            blinkt.set_pixel(7 - x, r, g, b)

    if mode == MODE_SEC:
        blinkt.set_pixel(0, 0, 0, 255)
        for x in range(6):
            bit = (s & (1 << x)) > 0
            r, g, b = [128 * bit] * 3
            blinkt.set_pixel(7 - x, r, g, b)

    blinkt.show()

    time_in_mode += 1
    if time_in_mode == time_to_stay_in_mode:
        mode += 1
        mode %= 3
        time_in_mode = 0

    time.sleep(1)

def show_all(state):
    for i in range(blinkt.NUM_PIXELS):
        val = state * 255
        blinkt.set_pixel(i, val, val, val)
    blinkt.show()

def dot():
    show_all(1)
    time.sleep(0.05)
    show_all(0)
    time.sleep(0.2)

def dash():
    show_all(1)
    time.sleep(0.2)
    show_all(0)
    time.sleep(0.2)

def space():
    time.sleep(0.2)

def morse_code():
    MORSE = '111101201211012110222'
    for m in MORSE:
        if m == '0':
            space()
        elif m == '1':
            dot()
        elif m == '2':
            dash()

def dash_red():
    blinkt.set_brightness(1)
    blinkt.set_all(255,0,0)
    blinkt.show()
    time.sleep(0.9)
    show_all(0)
    time.sleep(0.4)

def dot_blue():
    blinkt.set_brightness(1)
    blinkt.set_all(255,0,0)
    blinkt.show()
    time.sleep(0.05)
    show_all(0)
    time.sleep(0.2)

def clear():
    blinkt.clear()
    blinkt.show()
    time.sleep(0.5)

def solid_red():
    blinkt.set_all(255,0,0)
    blinkt.show()
    

def solid_green():
    blinkt.set_all(0,255,0)
    blinkt.show()
    

def solid_blue():
    blinkt.set_all(0,0,255)
    blinkt.show()
    

def solid_orange():
    blinkt.set_all(255,128,0)
    blinkt.show()
    

def solid_green_light():
    blinkt.set_all(0,20,0)
    blinkt.show()
    

def solid_white():
    blinkt.set_all(255,255,255)
    blinkt.show()
    
#-------Animationsbereich ENDE-------
			
