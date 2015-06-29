import skimage
from skimage import data
from bloblog import blobl
from blobdoh import blobh
from blobdog import blobg
from matplotlib import pyplot as plt
import os
from thresholding import threshold

image_list = ['RandSample/index-0/DSS--DSS2+IR_INVERT-NOLINES.png']

for i in range(20):
    dir = 'RandSample/index-'+str(i)+'/'
    files = [f for f in os.walk(dir)]
    for f in files[0][2]:
        if '_INVERT.png' in f and 'w4' not in f and 'NOLINES' not in f: #byproduct of my directory and pre-processing
            image_list.append(dir+'/'+f)
print image_list

rblob = 0
bblob = 0
yblob = 0

for image in image_list:
    threshold(image,image+'T.png')
    i=image+'T.png'
    log = blobl(i)
    dog = blobg(i)
    doh = blobh(i)
    plt.title(image)
    plt.draw()
    plt.pause(.2)
    correct = raw_input("How many blobs?")
    plt.close()
    rblob += (len(dog) - int(correct))
    bblob += (len(log) - int(correct))
    yblob += (len(doh) - int(correct))


print 'AVERAGE ERROR:'
print 'Difference of Gaussian:',float(rblob)/len(image_list)
print 'Laplacian of Gaussian:',float(bblob)/len(image_list)
print 'Determinant of Hessian:',float(yblob)/len(image_list)


#without threshold
#AVERAGE ERROR:
#Difference of Gaussian: 0.935483870968
#Laplacian of Gaussian: 0.709677419355
#Determinant of Hessian: -0.258064516129

#with threshold
#AVERAGE ERROR:
#Difference of Gaussian: -0.225806451613
#Laplacian of Gaussian: 3.38709677419
#Determinant of Hessian: 1.03225806452


### threshold turns diffraction spikes into diamonds, which the blob program can't handle -- definitely blob before threshold   
