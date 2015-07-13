'''
Greyscale image inversion

Laura Eckman 15/06/2015
'''

import os
import skimage
from skimage import data
from skimage import img_as_ubyte

max_index = int(raw_input('Max Index? (int): '))

#gathers image locations for given indices into images list
images = []
for i in range(1,max_index):
    dir = 'RandSample/index-'+str(i)
    files = [f for f in os.walk(dir)]
    for f in files[0][2]:
        if f != 'stellar_coordinates.txt' and '_INVERT.png' not in f:
            images.append(dir+'/'+f)
breaking = ['RandSample/index-3/WISE+(AllWISE)--w3','RandSample/index-3/WISE+(AllWISE)--w2']
for image in images:
    if image in breaking:
        continue
    print 'STARTED',image
    i = skimage.io.imread(image,True)
    img_as_ubyte(i)
    for k in range(len(i)):
        for j in range(len(i[0])):
            i[k][j] = 255 - i[k][j]
    dwn_file = image+'_INVERT.png'
    if not os.path.isfile(dwn_file):
        skimage.io.imsave(dwn_file,i)