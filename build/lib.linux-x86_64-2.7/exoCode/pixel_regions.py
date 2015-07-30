'''
program to identify pixels within a given region

Copyright (c) 2015, Laura Eckman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from math import sqrt, floor, ceil


def circle_points(radius,(x,y)):
    '''
    Return tuple ([border points (x,y)], [all points in circle (x,y)])
    Args: radius (int in pixels), (x,y) tuple marking center location
    '''
    encl = []
    border = []

    for i in range(-radius,radius+1):
        for j in range(-radius,radius+1):
            dist = sqrt(abs(i)**2 + abs(j)**2)
            if dist < radius+.5:
                encl.append((x+i,y+j))
                if dist > radius-.5:
                    border.append((x+i,y+j))

    return (border,encl)

def middle_box(dimensions):
    '''
    dimensions: (x pixel count, y pixel count) tuple
    Return middle 9th of square field as (x,y) coordinate list
    '''
    mid = (dimensions[0]/2.,dimensions[1]/2.)
    enclosed = []
    for i in range(int(floor(-dimensions[0]/6.+mid[0])),int(ceil(dimensions[0]/6.+mid[0]))):
        for j in range(int(floor(-dimensions[1]/6.)+mid[1]),int(ceil(dimensions[1]/6.+mid[1]))):
            enclosed.append((i,j))
    return enclosed

