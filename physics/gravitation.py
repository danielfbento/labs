from math import *
from numpy import *
from pylab import *
from random import *
from matplotlib.colors import LogNorm

def main():
    # Gravitational Constant
    G = 6.6738480E-11

    # grid options
    points = 500
    side = 100.0
    spacing = side/points

    # object at the center
    mass = 1
    xc = side/2
    yc = side/2
    
    # random object (not more massive than the first)
    seed()
    xi = randint(0,side)
    seed()
    yi = randint(0,side)
    seed()
    massi = random()*mass

    # gravitational field
    g = empty([points,points],float)

    # building the force field
    for i in range(points):
        y = spacing * i
        for j in range(points):
            x = spacing * j
            r = sqrt((x-xc)**2 + (y-yc)**2)
            ri = sqrt((x-xi)**2 + (y-yi)**2)
            if r == 0 or ri == 0:
                g[i,j] = +inf
                continue
            g[i,j] =  G * (mass / r**2) + G* (massi / ri**2)

    # it is represented in logarithm scale!
    figure()
    imshow(g,origin="lower",extent=[0,side,0,side],norm=LogNorm())
    show()

if __name__ == "__main__":
    main()
