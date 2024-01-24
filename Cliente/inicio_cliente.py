try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network
import time

import gc
gc.collect()
time.sleep_ms(500)

led = Pin("LED", Pin.OUT)
led.off()

ssid = 'Pico-W-Andres'
password = '123456789'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  print('Connecting........')
  time.sleep_ms(500)
  

print('Connection successful')
print(station.ifconfig())

led.on()