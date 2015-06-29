'''
Blob detection in astronomical images using various options in scikit-image module 

Laura Eckman 18/06/15
'''

import skimage

from matplotlib import pyplot as plt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray

image2 = skimage.io.imread('RandSample/index-0/DSS--DSS2+IR_INVERT-THRESHOLD-NOLINES.png',True)
image = skimage.io.imread('RandSample/index-0/DSS--DSS2+IR_INVERT-NOLINES.png',True)

blobs_log = blob_log(image, max_sigma=30, num_sigma=10, threshold=.1)
blobs_log2 = blob_log(image2, max_sigma=30, num_sigma=10, threshold=.1) #check these parameters in documentation
# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
blobs_log2[:, 2] = blobs_log2[:,2] * sqrt(2)

blobs_dog = blob_dog(image, max_sigma=30, threshold=.1)
blobs_dog2 = blob_dog(image2, max_sigma=30, threshold=.1)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)
blobs_dog2[:, 2] = blobs_dog2[:, 2] * sqrt(2)

blobs_doh = blob_doh(image, max_sigma=30, threshold=.01)
blobs_doh2 = blob_doh(image2, max_sigma=30, threshold=.01)

blobs_list = [blobs_log, blobs_dog, blobs_doh]
colors = ['yellow', 'lime', 'red']
titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
          'Determinant of Hessian']
sequence = zip(blobs_list, colors, titles)

blobs_list2 = [blobs_log2, blobs_dog2, blobs_doh2]
colors2 = ['yellow', 'lime', 'red']
titles2 = ['Laplacian of Gaussian', 'Difference of Gaussian',
          'Determinant of Hessian']
sequence2 = zip(blobs_list2, colors2, titles2)



fig, axes = plt.subplots(nrows=2,ncols=3,sharex=False,sharey=False)
for i in range(len(sequence)):
    axes[0,i].set_title(sequence[i][2])
    axes[0,i].imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    for blob in sequence[i][0]:
        y, x, r = blob
        c = plt.Circle((x, y), r, color=sequence[i][1], linewidth=2, fill=False)
        axes[0,i].add_patch(c)
for i in range(len(sequence2)):
    axes[1,i].set_title(sequence2[i][2])
    axes[1,i].imshow(image2, cmap=plt.cm.gray, interpolation='nearest')
    for blob in sequence2[i][0]:
        y, x, r = blob
        c = plt.Circle((x, y), r, color=sequence2[i][1], linewidth=2, fill=False)
        axes[1,i].add_patch(c)


for i in fig.axes:
    i.get_xaxis().set_visible(False)
    i.get_yaxis().set_visible(False)

axes[0,0].get_yaxis().set_visible(True)
axes[0,0].set_ylabel('Original Image')
axes[0,0].tick_params(labelsize=0)
axes[1,0].get_yaxis().set_visible(True)
axes[1,0].set_ylabel('Thresholded Image')
axes[1,0].tick_params(labelsize=0)

plt.subplots_adjust(left = 0.125, right = 0.9, bottom = 0.1, top = 0.9, wspace = 0.2, hspace = 0.2)
plt.axis('off')
plt.show()
