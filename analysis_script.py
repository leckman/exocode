'''
Analysis script for automation of disk detection program

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

import skimage
from skimage import data
from matplotlib import pyplot as plt
import os
import pyfits
import numpy as np
import time
import operator
from math import sqrt

from img_array.bloblog import blobl
from img_array.blobdoh import blobh
from img_array.blobdog import blobg
from img_array.diffraction import diffract
from img_array.thresholding import threshold


#load image arrays

def lingray(x, a=None, b=None):
    """
    Auxiliary function that specifies the linear gray scale.
    a and b are the cutoffs : if not specified, min and max are used
    Prancer Physics Louisville
    """
    if a == None:
        a = np.min(x)
    if b == None:
        b = np.max(x)
    return 255.0 * (x-float(a))/(b-a)

image_list = []

for i in range(10):
    dir = 'RandSample/FITS/index-'+str(i)
    files = [f for f in os.walk(dir)]
    for f in files[0][2]:
        if 'stellar' not in f and ('DSS' in f): #byproduct of my directory and pre-processing
            image_list.append(dir+'/'+f)
####
'''
BROKEN: 
2MASS AND WISE IMAGES STILL DEALING WITH "ValueError: Images of type float must be between -1 and 1."
'''
####

arrays = []

for i in image_list:
    inhdulist = pyfits.open(i)
    image_data = inhdulist[0].data
    new_image_data = lingray(image_data)
    arrays.append((new_image_data,i))
    inhdulist.close()

for array in arrays:
    img = array[0]
    title = array[1]
    center = round(len(img)/2.)
    if img==None:
        continue

    diffraction_points = diffract(img)
    blobs = blobl(img)

    central = {}
    for blob in blobs:
        if blob in diffraction_points:
            central[blob] = blobs[blob]

    main_row, main_col = max(central.iteritems(), key=operator.itemgetter(1))[0]
    distance = sqrt((main_row-center)**2 + (main_col-center)**2)


#show figures of interest
    plt.draw()
    if distance > 2 or len(central)>1:
        plt.pause(1.2)
    plt.close()


