
'''
Corrects for borders left on some 2MASS and DSS images so 
they are not mistaken for artifacts of interest in analysis

Laura Eckman 18/05/2015
'''

import skimage
from skimage import data
from skimage.util import img_as_ubyte
import matplotlib.pyplot as plt

def border_fill(input_file,save=False,output='',display=True):
    '''
    Args:
        input_file: string representing file location of image to process
        save: bool, saves to disc if True
        output: string representing output location for processed image, 
            program will prompt for location if this is empty and save is True
        display: bool, opens matplotlib display if True
    Returns none
    '''

    i = skimage.io.imread(input_file,True)
    image = img_as_ubyte(i)

    #vertical lines
    vert = True
    countv = 0
    for i in range(len(image[0])-1):
        if image[0][i] == image[0][i+1]:
            countv += 1
        else:
            break
    for i in range(len(image)-1):
        for j in range(countv-1):
            if image[i][j] != image[i][j+1] or image[i][j] != image [i+1][j]:
                vert = False
                break

    #horizonal lines
    horz = True
    counth = 1
    for i in range(1,len(image)):
        if image[-i][-1] == image[-(i+1)][-1]:
            counth += 1
        else:
            break
    for i in range(1,counth-1):
        for j in range(len(image[0])-1):
            if image[-i][j] != image[-(i+1)][j] or image[-i][j] != image[-i][j+1]:
                horz = False
                break

    #fill border artifacts
    if horz:
        h_col = abs(255-image[-1][-1])
        for i in range(1,counth+1):
            for j in range(len(image[0])):
                image[-i][j] = h_col

    if vert:
        v_col = abs(255-image[0][0])
        for i in range(len(image)):
            for j in range(countv+1):
                image[i][j] = v_col

    if display:
        fig, ax = plt.subplots(1, 1)
        ax.imshow(image, cmap=plt.cm.gray)
        ax.set_title('Input image')
        ax.axis('image')
        plt.show()
    
    if save:
        while not output:
            output = raw_input('Save location? ')
        skimage.io.imsave(output,image)


