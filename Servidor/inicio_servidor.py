try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import gc
gc.collect()

led = Pin("LED", Pin.OUT)
led.off()

ssid = 'Pico-W-Andres'
password = '123456789'

ap = network.WLAN(network.AP_IF)

ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())
print(ap.config('ssid'))

led.on()