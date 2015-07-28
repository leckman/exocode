'''
Blob detection in astronomical images using various options in scikit-image module 

No arrangement of parameters gives a reliable detection of WISE blob

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
from skimage.feature import blob_doh
import numpy as np
from thresholding import threshold

def blobh(image,out_file='',display=False):
    '''
    Determinant of Hessian Implementation for scikit-image blob detection
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
    Returns dict of detected blobs (fmt: {position tuple:radius})

    OBSOLETE
        NO ARRANGEMENT OF PARAMETERS GIVES RELIABLE DETECTION IN WISE BANDS
    '''
    dimensions = [len(image),len(image[0])]
    min_sigma = 1.
    max_sigma = 30.
    num_sigma = 1.
    thresh = threshold(image)[1]
    overlap = 0.5
    log_scale = True
    blobs_doh = blob_doh(image,min_sigma,max_sigma,num_sigma,
         thresh,overlap,log_scale)

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    blob_dict = {}
    for blob in blobs_doh:
        y, x, r = blob
        if r >= 0.4*dimensions[0] or r >= 0.4*dimensions[1] or r <= 1:
            continue
        blob_dict[(x,y)] = r
        c = plt.Circle((x,y), r, color='y', linewidth=2, fill=False)
        center = plt.Circle((x,y),.5,color ='y',linewidth=0.5,fill=True)
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
