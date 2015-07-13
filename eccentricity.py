'''
Calculate eccentricty of an ellipse given the side lengths of the containing rectangle
Laura Eckman 07/2015
'''

import math

def eccentricity(len1,len2):
    '''
    Params: numerical representations of rectangle side lengths
    Returns: eccentricity of ellipse bounded by those side lengths as float
    '''
    if len1 > len2:
        a = len1/2.0
        b = len2/2.0
    else:
        a = len2/2.0
        b = len1/2.0
    c = math.sqrt(a**2-b**2)
    return c/a