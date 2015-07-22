
'''
Very basic command-line interface for determining the validity of the dependent blob detection programs on the given dataset

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

import skimage
from skimage import data
from img_array.bloblog import blobl
from img_array.blobdoh import blobh
from img_array.blobdog import blobg
from matplotlib import pyplot as plt
import os
from img_array.thresholding import threshold
import pyfits
import numpy as np
import time

def lingray(x, a=None, b=None):
    """
    Auxiliary function that specifies the linear gray scale.
    a and b are the cutoffs : if not specified, min and max are used
    Prancer Physics Louisville
    """
    if a == None:
        a = np.min(x)
    if b == None:
        b = np.max(x)
    return 255.0 * (x-float(a))/(b-a)

def loggray(x, a=None, b=None):
    """
    Auxiliary function that specifies the logarithmic gray scale.
    a and b are the cutoffs : if not specified, min and max are used
    Prancer Physics Louisville
    """
    if a == None:
        a = np.min(x)
    if b == None:
        b = np.max(x)          
    linval = 10.0 + 990.0 * (x-float(a))/(b-a)
    return (np.log10(linval)-1.0)*0.5 * 255.0

image_list = []

for i in range(5):
    dir = 'RandSample/FITS/index-'+str(i)
    files = [f for f in os.walk(dir)]
    for f in files[0][2]:
        if 'stellar' not in f and 'DSS' in f: #byproduct of my directory and pre-processing
            image_list.append(dir+'/'+f)
#print image_list

rblob = 0
bblob = 0
yblob = 0

arrays = dict.fromkeys(image_list)

for i in image_list:
    inhdulist = pyfits.open(i)
    image_data = inhdulist[0].data
    new_image_data = lingray(image_data)
    arrays[i]=new_image_data
    inhdulist.close()
terribleness = 0
for array in arrays:
    i = arrays[array]
    if i==None:
        continue
    new = i
    print 'INDEX:',image_list.index(array)
    start_log = time.time()
    log = blobl(new)
    print 'LOG TIME:', time.time() - start_log
    start_dog = time.time()
    print 'DOG TIME:', time.time() - start_dog
    dog = blobg(new)
    start_doh = time.time()
    #doh = blobh(new)
    #print 'DOH TIME:',time.time()-start_doh
    plt.title(array)
    plt.draw()
    plt.pause(.2)
    terribleness += int(raw_input("Enter to continue: "))
    plt.close()


print float(terribleness)/len(arrays)

###BLOBLOG###

#Indices 0-4
#Run: 0.286
#Run: 0.381 (outsourced to Liam)

#Indices 5-9
#Run: 0.4
#Run: 0.12 (outsourced to Liam)

#DOG is nearly 7000x faster than LOG (.2-.4 sec for log compared to 2e-06 - 3e-06 for dog)


