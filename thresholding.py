'''
Use Otsu's method to analyze catalog images, keep pixels only above a certain threshold

Laura Eckman 15/06/2015
'''

import matplotlib.pyplot as plt
import skimage
from skimage import data
from skimage.filters import threshold_otsu
from skimage.util import img_as_ubyte


def threshold(input_file,output_file):
    '''
    Args:
      input_file: string representing location of 
        image to be analysed
      output_file: string representing location where 
        thresholded image should be saved
    Process image and save thresholded version
    Return threshold value
    '''
    #import as greyscale, convert to array
    i = skimage.io.imread(input_file,True)
    img = img_as_ubyte(i)

    #threshold
    threshold_global_otsu = threshold_otsu(img)
    global_otsu = img >= threshold_global_otsu

    fig = plt.imshow(global_otsu,cmap=plt.cm.gray)
    #removes whitespace and axes on figure
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    #saves resulting figure to file
    plt.savefig(output_file,bbox_inches='tight',pad_inches=0)

    return threshold_global_otsu

