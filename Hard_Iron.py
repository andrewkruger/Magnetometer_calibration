import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from mpl_toolkits.mplot3d import Axes3D


def calc_params3(xc, yc, zc, xm, ym, zm):
    return (((x3-xc)/xm)**2 + ((y3-yc)/ym)**2 + ((z3-zc)/zm)**2)    
    
def lq_function3(c):
    fit = calc_params3(*c)
    return fit - 1

    #get parameter estimates
x3_cen = (x3.max()+x3.min())/2.
y3_cen = (y3.max()+y3.min())/2.
z3_cen = (z3.max()+z3.min())/2.
x3_mag = (x3.max()-x3.min())/2.
y3_mag = (y3.max()-y3.min())/2.
z3_mag = (z3.max()-z3.min())/2.

    #fit data
params3_estimate = x3_cen, y3_cen, z3_cen, x3_mag, y3_mag, z3_mag
params3, ier = optimize.leastsq(lq_function3, params3_estimate)
xc_3, yc_3, zc_3, xm_3, ym_3, zm_3 = params3

    #calibrate data
x3_hcal = (x3-xc_3)/xm_3
y3_hcal = (y3-yc_3)/ym_3
z3_hcal = (z3-zc_3)/zm_3

    #plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
ax.view_init(20,-150)
ax.autoscale_view(tight=True)
ax.scatter(x3_hcal,y3_hcal,z3_hcal)
#ax.plot(np.zeros(npts_fit),xunit,yunit,color='r')
#ax.plot(xunit,np.zeros(npts_fit),yunit,color='r')
#ax.plot(xunit,yunit,np.zeros(npts_fit),color='r')
plt.show()
