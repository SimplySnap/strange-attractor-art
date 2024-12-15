import random
import math
from time import time
from matplotlib import pyplot

n = 12
found = 0
t_start = -2
t_end = 2

while found < n:
    x = random.uniform(-0.5,0.5)
    y = random.uniform(-0.5,0.5)

    #random alternative point nearby - perturb x,y by epsilon
    xe = x + random.uniform(-0.5, 0.5)/1000
    ye = y + random.uniform(-0.5,0.5)/1000

    #distance between two points
    dx = xe-x
    dy = ye-y
    d0 = math.sqrt(dx*dx + dy*dy) #sqrt distance

    a = [random.uniform(-2,2) for i in range(17)]

    #lists to store the path, which we graph
    x_list = [x]
    y_list = [y]

    #initialising convergence boolean and lyapunov exponent
    lyapunov = 0
    converging = False

    #main generating loop
    t = t_start
    for i in range(10000):
        xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y + a[6]*x*t + a[7]*y*t + a[8]*x
        ynew = a[9] + a[9]*x + a[10]*x*x + a[11]*y + a[12]*y*y + a[13]*x*y + a[14]*x*t + a[15]*y*t + a[16]*x

        #Checking for convergence to infinity to rule out
        if abs(xnew) > 1e10 or abs(ynew) > 1e10: 
            converging = True
            break

        #check if we converge to a single value
        if abs(x-xnew) < 1e-10 and abs(y-ynew) < 1e-10: 
            converging = True
            break

        #checking for chaotic behaviour
        if i > 1000:
            #compute next alternative point
            xenew = a[0] + a[1]*xe + a[2]*xe*xe + a[3]*ye + a[4]*ye*ye + a[5]*xe*ye
            yenew = a[6] + a[7]*xe + a[8]*xe*xe + a[9]*ye + a[10]*ye*ye + a[11]*xe*ye

            dx = xenew - xe
            dy = yenew - ye
            d = math.sqrt(dx*dx + dy*dy)

            #update the lyapunov exponent
            lyapunov += math.log(abs(d/d0))

            #rescale alternate point
            xe = xnew + d0*dx/d
            ye = ynew + d0*dy/d


        #updating (x,y)
        x = xnew
        y = ynew
        t = t + i/1000*4

        x_list.append(x)
        y_list.append(y)
    
    #Checking if we have found chaotic behaviour
    if not converging and lyapunov >= 100:
        found +=1;
        print("We found a strange attractor with L = "+ str(lyapunov))

        #clear figure
        pyplot.clf()

        #pyplot design
        pyplot.style.use('dark_background')
        pyplot.axis('off')

        pyplot.scatter(x_list[100:], y_list[100:], s = 0.1, c = 'white', linewidth = 0,)

        pyplot.savefig('pics/' + str(time()) + '.png', dpi = 200)
        #pyplot.show()