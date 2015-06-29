'''
program to identify pixels within a circle

Laura Eckman 29/06/2015
'''

import skimage
from math import sqrt
from skimage import data


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



