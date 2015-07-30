import skimage
from skimage import data
from skimage.util import img_as_ubyte
import matplotlib.pyplot as plt
import pyfits     

i = skimage.io.imread('RandSample/index-0/DSS--DSS2+IR_INVERT.png',True)
png_image = img_as_ubyte(i)

hdulist = pyfits.open('RandSample/FITS/index-0/DSS--DSS2+IR')
header_info = hdulist[0].header
fits_image = hdulist[0].data[::-1] #inverts because upside down

fig, axes = plt.subplots(1, 2)

axes[0].imshow(fits_image, cmap=plt.cm.gray)
axes[0].set_title('FITS image')
axes[0].axis('off')

axes[1].imshow(png_image, cmap=plt.cm.gray)
axes[1].set_title('PNG image')
axes[1].axis('off')

plt.show()
