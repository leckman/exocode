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
from skimage.feature import blob_log
from math import sqrt
import numpy as np
from pixel_regions import middle_box

def blobl(image,out_file='',display=False):
    '''
    LaPlacian of Gaussian implementation of scikit-image blob detection program
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
    Returns dict of detected blobs (fmt: {position tuple:radius})
    '''

    #blobs_log args for convenience
    dimensions = [len(image),len(image[0])]
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

    if out_file:
        plt.savefig(out_file,bbox_inches='tight',pad_inches=0)
    if display:
        plt.show()
    return blob_dict
