import random
import math
import time
from matplotlib import pyplot

n = 1 # Number of attractors we want to create
found = 0
transient = 500 # Number of transient iterations to skip when calculating lyapunov exponent


#Setup mpl enviro
#Artefacts
#pyplot.clf()
#pyplot design
pyplot.style.use('dark_background')
#pyplot.figure(facecolor='black') #To make sure the background is black
pyplot.axis('off')

pyplot.ion()

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
    #x_list = [x]
    #y_list = [y]
    x_cur = []
    y_cur = []

    #initialising convergence boolean and lyapunov exponent
    lyapunov = 0.0
    converging = False

    #main generating loop
    for i in range(20000): #Number of points
        xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y
        ynew = a[6] + a[7]*x + a[8]*x*x + a[9]*y + a[10]*y*y + a[11]*x*y

        #Checking for convergence to infinity to rule out
        if abs(xnew) > 1e10 or abs(ynew) > 1e10: 
            converging = True
            break

        #check if we converge to a single value
        if abs(x-xnew) < 1e-10 and abs(y-ynew) < 1e-10 and i > transient:
            #Transition period 
            converging = True
            break

            #  Update alternate point at transient time
        if i == transient:
            # After the transient phase, reset the perturbation
            xe = x + random.uniform(-0.5, 0.5) / 1000
            ye = y + random.uniform(-0.5, 0.5) / 1000

            dx = xe - x
            dy = ye - y
            d0 = math.sqrt(dx*dx + dy*dy)

        #checking for chaotic behaviour
        if i > transient:
            #compute next alternative point
            xenew = a[0] + a[1]*xe + a[2]*xe*xe + a[3]*ye + a[4]*ye*ye + a[5]*xe*ye
            yenew = a[6] + a[7]*xe + a[8]*xe*xe + a[9]*ye + a[10]*ye*ye + a[11]*xe*ye

            dx = xenew - xnew
            dy = yenew - ynew
            d = math.sqrt(dx*dx + dy*dy)

            #update the lyapunov exponent - use eps to prevent problems with convergence
            eps = 1e-10
            lyapunov += math.log((d + eps) / (d0 + eps))
            #lyapunov = lyapunov / (i - 1000)

            #rescale alternate point
            scaling_factor = d0 / d  if d != 0 else 1.0 #To keep scaling constant over iterations + numerical stability
            xe = xnew + dx * scaling_factor
            ye = ynew + dy * scaling_factor

        #updating (x,y)
        x = xnew
        y = ynew

        x_cur.append(x)
        y_cur.append(y)
    
    #Checking if we have found chaotic behaviour
    lyapunov = lyapunov / (20000 - transient) # Rescale lyapunov exponent
    if not converging and lyapunov > 0:
        found +=1;
        print("We found a strange attractor with Lyapunov exponent "+ str(lyapunov)) 
        
        #Loop for dynamic visualisation
    

        pyplot.scatter(x_cur, y_cur, s = 0.1, c = 'white', linewidth = 0)
        pyplot.draw()
        pyplot.pause(4)
        pyplot.gcf().canvas.draw_idle()  # Ensures full render!!
        pyplot.gcf().canvas.flush_events()

        #Save figure in pics folder - NO
        pyplot.savefig('pics/' + str(time.time()) + '.png', dpi = 500,transparent=False)
        #Plot attractor
#pyplot.ioff() # remove to start working on next steps

pyplot.show()