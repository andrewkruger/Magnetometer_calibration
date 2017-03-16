import time
import Adafruit_LSM303

#Copy fit parameters here:




lsm303 = Adafruit_LSM303.LSM303()

while True:
    accel, mag = lsm303.read()
    x, z, y = mag
    print "%.3f\t%.3f\t%.3f" % ((x-xc)/xm, (y-yc)/ym, (z-zc)/zm)
    time.sleep(0.1)
