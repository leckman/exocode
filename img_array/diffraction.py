'''
calculates and draws diffraction-limited circle onto different band images
w/ help from Tam Nguyen

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

from matplotlib import pyplot as plt
from pixel_regions import circle_points

##################################################################################
'''
wavelengths and angular resolutions of different images
    {band: [wavelength (m), aperture (m), known angular resolution (arcmin)]}
***not currently in use: currently only using w4 band in calculations***
'''

bands = {
    'w1': (3.4, 0.4, 6.1/60),
    'w2': (4.6, 0.4, 6.4/60),
    'w3': (12., 0.4, 6.5/60),
    'w4': (22., 0.4, 12./60),
    'J': (1.25, 1.3, 2.4/60),
    'H': (1.65, 1.3, 3.2/60),
    'K': (2.17, 1.3, 4.2/60),
    'DSS2+Blue': (0.665, 1.22, 1.4/60),   #calculated out, questionable
    'DSS2+Red': (0.975, 1.22, 2.0/60),    #calculated out, questionable
    'DSS2+IR': (1.15, 1.22, 2.5/60)       #calculated out, questionable
    }

#################################################################################

def diffract(image,out_file='',display=False):
    '''
    Applies diffraction circle to image (based on WISE w4 angular resolution of 12")
    Args:
      image: numpy array
      out_file: str representing save location of processed image (if not empty)
      display: bool to display image as matplotlib figure
    Returns list of (x,y) points inside diffraction circle
    '''
    angular_width=1.0  #arcmin

    #R(1.22*wave/aperture)*180/3.14*60 #arcmin
    angular_res = 12./60 #largest, corresponds to w4 band

    img_width = len(image) #pixels
    radius = angular_res*img_width/angular_width
    center = round(img_width/2)

    fig = plt.imshow(image,cmap=plt.cm.gray,interpolation='nearest')
    crosshairs = fig.axes.plot([center], [center],
        linestyle='none', marker='+',mew=2,ms=10,color='MediumVioletRed')
    c = plt.Circle((center,center), radius, color='MediumVioletRed', linewidth=2, fill=False)
    fig.axes.add_patch(c)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    if out_file:
        plt.savefig(out_file,bbox_inches='tight',pad_inches=0)

    if display:
        plt.title(array)
        plt.draw()
        plt.pause(.2)
        raw_input("Enter to continue: ")
        plt.close()

    return circle_points(int(round(radius)),(center,center))[1]


