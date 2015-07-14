'''
Use Otsu's method to analyze catalog images, keep pixels only above a certain threshold

Laura Eckman 15/06/2015
'''

from skimage.filters import threshold_otsu



def threshold(img):
    '''
    Args:
      img: numpy array of image
      output_file: string representing location where 
        thresholded image should be saved
    Process image and save thresholded version
    Return (thresholded array,threshold value)
    '''

    #threshold
    threshold_global_otsu = threshold_otsu(img)
    global_otsu = img >= threshold_global_otsu

    return (global_otsu,threshold_global_otsu)

