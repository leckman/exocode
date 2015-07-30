'''
Blob detection in astronomical images using various options in scikit-image module 

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

from matplotlib import pyplot as plt
from skimage.feature import blob_log, blob_doh
from math import sqrt
import numpy as np
from pixel_regions import middle_box
from thresholding import threshold as thresh

def blobl (image,survey):
    '''
    LaPlacian of Gaussian implementation of scikit-image blob detection program
    WISE images: >85% accuracy with given params. No false positives seen. 
    
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
    Returns dict of detected blobs (fmt: {position tuple:radius})
    '''
    dimensions = [len(image),len(image[0])]

    #blob_log args for convenience
    if survey == 'WISE':
        min_sigma = 1.
        max_sigma = 30.
        num_sigma = 30.
        threshold = thresh(image)[1]
        overlap = 1.0
        log_scale = False
    elif survey == 'DSS':
        min_sigma = 3.
        max_sigma = 30.
        num_sigma = 20.
        threshold = 12.
        overlap = 1.0
        log_scale = False

    blobs_log = blob_log(image,min_sigma,max_sigma,num_sigma,
        threshold,overlap,log_scale)

    if blobs_log.any():
        blobs_log[:,2] = blobs_log[:,2] * sqrt(2) #radius is ~sqrt(2)*sigma

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    blob_dict = {}
    for blob in blobs_log:
        y, x, r = blob
        if ((r>.25*dimensions[1] or r>.25*dimensions[1]) and 
            (y in (0,dimensions[0]) or x in (0,dimensions[0]))):
            continue
        if (x,y) not in middle_box(dimensions) and r <= 1:
            continue
        blob_dict[(x,y)] = r
        c = plt.Circle((x,y), r, color='b', linewidth=2, fill=False)
        center = plt.Circle((x,y),.5,color ='b',linewidth=0.5,fill=True)
        fig.axes.add_patch(c)
        fig.axes.add_patch(center)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    return blob_dict

def blobdoh_2MASS(image):
    '''
    Determinant of Hessian Implementation for scikit-image blob detection
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
    Returns dict of detected blobs (fmt: {position tuple:radius})

    Works great & fast with 2MASS images using default parameters, including auxilliary blobs
    BEST for 2MASS
    '''
    dimensions = [len(image),len(image[0])]

    blobs_doh = blob_doh(image)

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    blob_dict = {}
    for blob in blobs_doh:
        y, x, r = blob
        if r >= 0.4*dimensions[0] or r >= 0.4*dimensions[1]:
            continue
        blob_dict[(x,y)] = r
        c = plt.Circle((x,y), r, color='y', linewidth=2, fill=False)
        center = plt.Circle((x,y),.5,color ='y',linewidth=0.5,fill=True)
        fig.axes.add_patch(c)
        fig.axes.add_patch(center)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    return blob_dict
