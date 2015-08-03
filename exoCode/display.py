'''
Displays all images in a given target folder for convenient visual validation

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

import pyfits
from matplotlib import pyplot as plt
import os
from final_blob_identification import blobl, blobdoh_2MASS as blobh
from diffraction import diffract
from thresholding import threshold
from array_processing import lingray, loggray

##############

def display(target):
    image_links = []
    data_container = 'FITS/TAM/' #alter to analyze a different set
    folder = data_container+'index-'+str(target)
    files = [f for f in os.walk(folder)]
    for f in files[0][2]:
        if 'stellar' not in f and 'directory' not in f:
            image_links.append(folder+'/'+f)

    img_2MASS = []
    img_WISE = []
    img_DSS = []
    
    angular_width=1.0  #arcmin
    angular_res = 12./60 #largest, corresponds to w4 band

    for link in image_links:
        inhdulist = pyfits.open(link)
        image_data = inhdulist[0].data
        if 'DSS' in link:
            new_image_data = lingray(image_data,'DSS')
            img_width = len(new_image_data) #pixels
            radius = angular_res*img_width/angular_width
            center = int(round(img_width/2))
            img_DSS.append((new_image_data,link,(img_width,radius,center)))
        else:
            new_image_data = loggray(image_data)
            if '2MASS' in link:
                img_width = len(new_image_data) #pixels
                radius = angular_res*img_width/angular_width
                center = int(round(img_width/2))
                img_2MASS.append((new_image_data,link,(img_width,radius,center)))
            else:
                img_width = len(new_image_data) #pixels
                radius = angular_res*img_width/angular_width
                center = round(img_width/2)
                img_WISE.append((new_image_data,link,(img_width,radius,center)))
        inhdulist.close()
    if len(img_2MASS) > 4 and len(img_2MASS) > len(img_DSS):
        max_plot = len(img_2MASS)
    elif len(img_DSS) > 4:
        max_plot = len(img_DSS)
    else:
        max_plot = 4

    fig, axes = plt.subplots(3, max_plot)
    img_2MASS.sort(key=lambda x: x[1])
    img_WISE.sort(key=lambda x: x[1])
    img_DSS.sort(key=lambda x: x[1])

    for i in range(len(img_2MASS)):
        img_width,radius,center = img_2MASS[i][2]
        axes[0][i].imshow(img_2MASS[i][0], cmap=plt.cm.bone)
        axes[0][i].set_title(img_2MASS[i][1].split('/')[3])
        crosshairs = axes[0][i].plot([center], [center],
            linestyle='none', marker='+',mew=2,ms=10,color='MediumVioletRed')
        c = plt.Circle((center,center), radius, color='MediumVioletRed', linewidth=2, fill=False)
        axes[0][i].add_patch(c)
    
    for i in range(len(img_DSS)):
        img_width,radius,center = img_DSS[i][2]
        axes[1][i].imshow(img_DSS[i][0], cmap=plt.cm.bone)
        axes[1][i].set_title(img_DSS[i][1].split('/')[3])
        crosshairs = axes[1][i].plot([center], [center],
            linestyle='none', marker='+',mew=2,ms=10,color='MediumVioletRed')
        c = plt.Circle((center,center), radius, color='MediumVioletRed', linewidth=2, fill=False)
        axes[1][i].add_patch(c)

    for i in range(len(img_WISE)):
        img_width,radius,center = img_WISE[i][2]
        axes[2][i].imshow(img_WISE[i][0], cmap=plt.cm.bone)
        axes[2][i].set_title(img_WISE[i][1].split('/')[3])
        crosshairs = axes[2][i].plot([center], [center],
            linestyle='none', marker='+',mew=2,ms=10,color='MediumVioletRed')
        c = plt.Circle((center,center), radius, color='MediumVioletRed', linewidth=2, fill=False)
        axes[2][i].add_patch(c)
    for i in axes:
        for j in i:
            j.axis('off')
    plt.show()

