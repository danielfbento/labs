#!/usr/bin/python
#
# @file: interpolation.py
# @date: 14-02-2013
# @lastmodified: Mon 18 Feb 2013 10:46:50 AM WET
#
# @author:danielfbento <danielbento@overdestiny.com
#
# @description: Interpolate video frames and produce new frames with the
# double size in dimensions using interpolation method
#

__author__ = "Daniel Bento"
__copyright__ = "Daniel Bento"
__licence__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Daniel Bento"
__email__ = "danielbento@overdestiny.com"
__status__ = "development"

from numpy import *
from pylab import *
import Image
import cv
import math

def function_interp(p1,p2):
    a = float(p1)
    b = float(p2)
    if a > b:
        i = a - abs(a-b)/2
    if a < b:
        i = a + abs(a-b)/2
    if a == b:
        i = a
    return i

def interpolate(p1,p2):
    #a = float(p1)
    #b = float(p2)
    #i = (a+b)/2
    #i = a + (a-b)*sin(math.pi/4)
    #return [p1,int(i),p2]
    r = int(function_interp(p1[0],p2[0]))
    g = int(function_interp(p1[1],p2[1]))
    b = int(function_interp(p1[2],p2[2]))
    return [[p1[0],p1[1],p1[2]],[r,g,b],[p2[0],p2[1],p2[2]]]

def main():
    
    capture = cv.CaptureFromFile("sem.mp4")
    a = 0
    while a < 100:
        a = a + 1
        img = cv.QueryFrame(capture)

        tmp = cv.CreateImage(cv.GetSize(img),8,3)
        cv.CvtColor(img, tmp, cv.CV_BGR2HSV)
        cv.CvtColor(tmp, tmp, cv.CV_HSV2RGB)

        matrix = asarray(cv.GetMat(tmp))

        result = zeros((len(matrix)*2-1,len(matrix[0])*2-1,3),'uint8')
    
        i = 0
        m = i
        while i < (len(matrix)-1) and m < (len(result) - 2):
            j = 0
            k = j
            while j < (len(matrix[i]) - 1) and k < (len(result[i])-2):
                c = interpolate(matrix[i][j],matrix[i][j+1])
                l = interpolate(matrix[i][j],matrix[i+1][j])

                result[m][k] = c[0]
                
                result[m][k+1] = c[1]
                result[m][k+2] = c[2]
                
                result[m+1][k] = l[1]
                result[m+2][k] = l[2]

                c = interpolate(matrix[i+1][j],matrix[i+1][j+1])
                l = interpolate(matrix[i][j+1],matrix[i+1][j+1])
                
                result[m+2][k+1] = c[1]
                result[m+2][k+2] = c[2]

                result[m+1][k+2] = l[1]

                mid = interpolate(result[m+1][k],result[m+1][k+2])

                result[m+1][k+1] = mid[1]

                j = j + 1
                k = k + 2

            i = i + 1
            m = m + 2
        img = Image.fromarray(result)
        #img.show()
        img.save('%d.png' % a)

if __name__ == "__main__":
    main()
