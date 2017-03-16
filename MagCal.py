import time
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Adafruit_LSM303

lsm303 = Adafruit_LSM303.LSM303()

x = []
y = []
z = []

#Functions used for fitting data
def calc_params3(xc3, yc3, zc3, xm3, ym3, zm3):
    return (((x-xc3)/xm3)**2 + ((y-yc3)/ym3)**2 + ((z-zc3)/zm3)**2)    
    
def lq_function3(c):
    fit = calc_params3(*c)
    return fit - 1

#Get data
ndat = 400
for i in range(ndat):
    accel, mag = lsm303.read()
    mag_x, mag_z, mag_y = mag
    print mag
    x.append(mag_x)
    y.append(mag_y)
    z.append(mag_z)
    time.sleep(0.03)

#plot raw data
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.set_xlabel('Mag X')
ax.set_ylabel('Mag Y')
ax.set_zlabel('Mag Z')
ax.scatter(x,y,z)
plt.show()



#get parameter estimates
x = np.array(x)
y = np.array(y)
z = np.array(z)
x_cen = (x.max()+x.min())/2.
y_cen = (y.max()+y.min())/2.
z_cen = (z.max()+z.min())/2.
x_mag = (x.max()-x.min())/2.
y_mag = (y.max()-y.min())/2.
z_mag = (z.max()-z.min())/2.

#fit data
params3_estimate = x_cen, y_cen, z_cen, x_mag, y_mag, z_mag
params3, ier = optimize.leastsq(lq_function3, params3_estimate)
xc, yc, zc, xm, ym, zm = params3

#calibrate data
xcal = (x-xc)/xm
ycal = (y-yc)/ym
zcal = (z-zc)/zm

#remove bad points
rmd = []
mag = np.sqrt(xcal**2+ycal**2+zcal**2)
sigma = np.std(mag)
var = 3*sigma
for i in range(ndat):
    if mag[i] > 1+var or mag[i] < 1-var:
        rmd.append(i)
x=np.delete(x,rmd)
y=np.delete(y,rmd)
z=np.delete(z,rmd)

#refit data
params3, ier = optimize.leastsq(lq_function3, params3_estimate)
xc, yc, zc, xm, ym, zm = params3
xcal = (x-xc)/xm
ycal = (y-yc)/ym
zcal = (z-zc)/zm


#print fit parameters
print '\nIf the data is all on the edge of the sphere, copy the'
print 'following and paste into Magnetometer.py:\n'
print 'xm =',xm
print 'ym =',ym
print 'zm =',zm
print 'xc =',xc
print 'yc =',yc
print 'zc =',zc


#make sphere
u = np.linspace(0, 2*np.pi, 21)
v = np.linspace(0, np.pi, 15)
xs = np.outer(np.cos(u), np.sin(v))
ys = np.outer(np.sin(u), np.sin(v))
zs = np.outer(np.ones(np.size(u)), np.cos(v))

#plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_aspect('equal')
ax.autoscale_view(tight=True)
ax.plot_surface(xs, ys, zs, rstride=1, cstride=1, \
    color='b', alpha=0.08, edgecolors='lightgrey', linewidth=1)
ax.scatter(xcal,ycal,zcal)
plt.show()
