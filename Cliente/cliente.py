from machine import Pin, SPI, I2C
from sdcard import SDCard
from ssd1306 import SSD1306_I2C
from utime import sleep_ms
from time import localtime
from uos import VfsFat, mount
from os import listdir
import inicio_cliente
import socket
        
def graficar(datos):
    X = 48

    fecha = localtime()
    oled.fill(0)
    oled.text("{dia:02d}/{mes:02d}/{año:04d} {hora:02d}:{minuto:02d}".format(año = fecha[0],mes = fecha[1],dia = fecha[2],hora = fecha[3],minuto = fecha[4]),0,0)
    oled.text("Wifi",X,8)
    oled.line(24,16,24,63,1)
    oled.line(24,16,127,16,1)

    maximo = max(datos)
        
    oled.text("{medio:02d}".format(medio=int(maximo/2)),0,36)
    oled.text("{max:02d}".format(max=int(maximo)),0,16)
        
    if not maximo == 0:
        ratio = 100/maximo
    else:
        ratio = 0
        
    for k in range(len(datos)):

        X = 128-(k+1)*8
        Y = int(64-48*datos[k]*ratio/100) 
        
        oled.rect(X+2,Y,6,64-Y,1,True)
        
    oled.show()

    while True:
        fecha = localtime()
        oled.rect(0,0,128,16,0,True)
        oled.text("{dia:02d}/{mes:02d}/{año:04d} {hora:02d}:{minuto:02d}".format(año = fecha[0],mes = fecha[1],dia = fecha[2],hora = fecha[3],minuto = fecha[4]),0,0)
        oled.text("Wifi",X,8)
        oled.text("Wifi",X+64,8)
        oled.text("Wifi",X+128,8)
        oled.text("Wifi",X-64,8)
        oled.text("Wifi",X-128,8)
        oled.show()
        X -= 1
        if X == -32:
            X = 160
        sleep_ms(40)
#-------------------------

#pantalla
WIDTH=128
HEIGHT=64
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT,i2c)
#-----------------------------------------

#SD
cs = Pin(13)
spi = SPI(1,
          baudrate=1000000,
          polarity=0,
          phase=0,
          sck = Pin(10),
          mosi = Pin(11),
          miso = Pin(12))

sd = SDCard(spi, cs)
vol = VfsFat(sd)
mount(vol, "/sd")
#---------------------

#Recopilar datos
datos = []
cont = 0

for ruta in listdir("/sd"):
    if cont >= 14:
        break
    if ruta[:5] == "Datos":
        archivo = open("/sd/"+ruta, "r")
        aux = archivo.read()
        archivo.close()
        
        cruces = 0
        
        for linea in aux.split("\n"):
            if linea == "":
                continue
            cruces += int(linea[:2])
        
        datos.insert(0,cruces)
        cont += 1
#---------------------------

#Envío de datos
while True:
    try:
        ai = socket.getaddrinfo("192.168.4.1", 80)
        addr = ai[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(str(datos))
        ss = str(s.recv(512),"utf-8")
        datos2 = list(ss[1:len(ss)-1].split(","))
        for i in range(len(datos2)):
            datos2[i] = int(datos2[i])
        graficar(datos2)
        
    except Exception as e:
        print(e)