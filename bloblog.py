'''
Blob detection in astronomical images using various options in scikit-image module 

Laura Eckman 18/06/15
'''

import skimage
from matplotlib import pyplot as plt
from skimage import data
from skimage.feature import blob_log
from math import sqrt
from astropy.io import fits
import numpy as np

def blobl(img_file,out_file='',display=False,fmt='png'):
    '''
    LaPlacian of Gaussian implementation of scikit-image blob detection program
    Args:
      img_file: str representing image location
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
      fmt: file extension, default 'png', alternatively 'FITS'
    Returns dict of detected blobs (fmt: {radius:position tuple}
    '''

    if fmt == 'png':
    	image = skimage.io.imread(img_file,True) #imports as greyscale
    elif fmt == 'FITS':
        image = fits.open(img_file)[0]
        image.scale('int16')
        image = image.data

    blobs_log = blob_log(image, max_sigma=30, num_sigma=10, threshold=.1)
    if blobs_log.any():
        blobs_log[:,2] = blobs_log[:,2] * sqrt(2)

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    blob_dict = {}
    for blob in blobs_log:
        y, x, r = blob
        blob_dict[r] = (x,y)
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
