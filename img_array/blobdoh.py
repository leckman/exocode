
from matplotlib import pyplot as plt
from skimage.feature import blob_doh
import numpy as np

def blobh(image,out_file='',display=False,fmt='png'):
    '''
    Determinant of Hessian Implementation for scikit-image blob detection
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
      fmt: file extension, default 'png', alternatively 'FITS'
    Returns dict of detected blobs (fmt: {radius:position tuple}
    '''

    blobs_doh = blob_doh(image,max_sigma=10,num_sigma=10, max_sigma=30, threshold = 0.01)

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    blob_dict = {}
    for blob in blobs_doh:
        y, x, r = blob
        blob_dict[r] = (x,y)
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
