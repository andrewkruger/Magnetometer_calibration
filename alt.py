import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import time

sealevel_pressure = 101520
n_avg = 5
n_data = 50
button_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
sensor = BMP085.BMP085()

#print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
#print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
#print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
#print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))

file_number = 1
alt_dat = 0
while(1):
        with open('data.txt','a') as myFile:
                for j in range(n_avg):
                        time.sleep(.1)
                        alt_dat+=sensor.read_altitude(sealevel_pa=sealevel_pressure)
                myFile.write(str(alt_dat/n_avg)+"\n")
                alt_dat = 0
