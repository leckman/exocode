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

from img_array.bloblog_WISE import blobl as WISE_blob
from img_array.blobdoh_2MASS import blobh as 2MASS_blob
from img_array.bloblog_DSS import blobl as DSS_blob
from img_array.diffraction import diffract
from img_array.thresholding import threshold
from img_array.array_processing import lingray, loggray


#load image arrays
targets = range(5)

def target_analysis(target):
    image_links = []

    folder = 'RandSample/FITS/index-'+str(target)
    files = [f for f in os.walk(folder)]
    for f in files[0][2]:
        if 'stellar' not in f:
            image_links.append(folder+'/'+f)

    arrays = []

    for link in image_links:
        inhdulist = pyfits.open(link)
        image_data = inhdulist[0].data
        if 'DSS' in link:
            new_image_data = lingray(image_data,'DSS')
        else:
            new_image_data = loggray(image_data)
        arrays.append((new_image_data,link))
        inhdulist.close()

    for array in arrays:
        img = array[0]
        title = array[1]
        center = round(len(img)/2.)
        if img==None:
            continue

        #throws out images where data has NaN errors
        if np.isnan(img).any():
            continue

        #throws out data bad in w3, w4 WISE band (no noticeable source)
        if 'w4' in title or 'w3' in title:
            num_pix = len(img)*len(img[0])
            white = 0
            for row in img:
                for col in row:
                    if col:
                        white += 1
            if float(white)/num_pix > 0.5:
                continue

        diffraction_points = diffract(img)
        blobs = blobl(img)

        #stats on blobs
        central = {}
        for blob in blobs:
            if blob in diffraction_points:
                central[blob] = blobs[blob]

        #throws out bad data (no noticeable source)
        if not central:
            continue
        
        main_row, main_col = max(central.iteritems(), key=operator.itemgetter(1))[0]
        distance = sqrt((main_row-center)**2 + (main_col-center)**2)


        #show figures of interest
        plt.title(title)
        plt.draw()
        if True: #distance > 2 or len(central)>1:
            plt.pause(1.0)
            raw_input('Enter to close: ')
        plt.close()


