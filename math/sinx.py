#!/usr/bin/python

import math
from pylab import *
import matplotlib.pyplot as plt

# n! Factorial of a number (Integer)
def fact(n):
    """ Returns n!
    """
    if (n == 0):
        return 1
    return n*fact(n-1)

# v^n Potentiation of a number (Real^Integer)
def poten(v,n):
    """ Returns v^n
    """
    r = 1
    if n == 0:
        return r
    for i in range(0,n):        
        r = v*r
    return r

# sin x = Sum{0..+Inf} (-1)^n/(2n+1)! * x^(2n+1)
def seno(x,terms):
    """ Returns sin x for a number of expansion terms
    """
    sen = 0
    for i in range(0,terms):
        sen = sen + (float(poten(-1,i)) / float(fact(2*i+1))) * float(poten(x,2*i+1)) 
    return sen

# output
def printv(n):
    if len(sys.argv) < 3:
        print "usage: %s range_start range_end" % sys.argv[0]
        return
    x0 = int(sys.argv[1])
    x1 = int(sys.argv[2])
    xr = range(x0,x1)
    y = [] 
    for j in xr:
        v = seno(math.pi/2,j)
        #print "%d terms: %f" % (j,v)
        y.append(v)    
    # we like plots :D
    #plt.plot(xr,y)
    #plt.show()
    xr = range(0,360)
    y = []
    for k in xr: 
        v = seno(float(k*2*math.pi)/360,10)
        y.append(v)
    plt.plot(xr,y)
    plt.show()

if __name__ == '__main__':
    printv(3)

