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
from skimage.feature import blob_dog
from math import sqrt
import numpy as np
from pixel_regions import middle_box
    
def blobg(image,out_file='',display=False):
    '''
    Difference of Gaussian implementation of scikit-image blob detection program
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
    Returns dict of detected blobs (fmt: {position tuple:radius})

    seems significantly less useful than the other two
    '''
    dimensions = (len(image),len(image[0]))
    min_sigma = 1. #min std dev
    max_sigma = 30. #max std dev
    sigma_ratio = 2.01 #ratio btwen std dev for difference computation
    threshold = 10. #lower bound, rules out less intense blobs
    overlap = 0.5

    blobs_dog = blob_dog(image,min_sigma,max_sigma,sigma_ratio,
        threshold,overlap)

    if blobs_dog.any():
        blobs_dog[:,2] = blobs_dog[:,2] * sqrt(2)

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    blob_dict = {}
    for blob in blobs_dog:
        y, x, r = blob
        if ((r>.25*dimensions[1] or r>.25*dimensions[1]) and 
            (y in (0,dimensions[0]) or x in (0,dimensions[0]))):
            continue
        if (x,y) not in middle_box(dimensions) and r <= 1:
            continue
        blob_dict[(x,y)] = r
        c = plt.Circle((x,y), r, color='r', linewidth=2, fill=False)
        center = plt.Circle((x,y),.5,color ='r',linewidth=0.5,fill=True)
        fig.axes.add_patch(c)
        fig.axes.add_patch(center)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    if out_file:
        plt.savefig(out_file,bbox_inches='tight',pad_inches=0)
    if display:
        plt.show()
    return blob_dict
