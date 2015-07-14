'''
Blob detection in astronomical images using various options in scikit-image module 

Laura Eckman 18/06/15
'''

from matplotlib import pyplot as plt
from skimage.feature import blob_dog
from math import sqrt
import numpy as np

def blobg(image,out_file='',display=False,fmt='png'):
    '''
    Difference of Gaussian implementation of scikit-image blob detection program
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
      fmt: file extension, default 'png', alternatively 'FITS'
    Returns dict of detected blobs (fmt: {radius:position tuple}
    '''

    blobs_dog = blob_dog(image, max_sigma=30, threshold=.1)
    if blobs_dog.any():
        blobs_dog[:,2] = blobs_dog[:,2] * sqrt(2)

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    blob_dict = {}
    for blob in blobs_dog:
        y, x, r = blob
        blob_dict[r] = (x,y)
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