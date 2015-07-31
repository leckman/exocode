'''
Analysis script for automation of disk detection program

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
from matplotlib import pyplot as plt
import os
import pyfits
import numpy as np
from math import sqrt

from final_blob_identification import blobl, blobdoh_2MASS as blobh
from diffraction import diffract
from thresholding import threshold
from array_processing import lingray, loggray
from pixel_regions import circle_points


#load image arrays

def target_analysis(target,data_container,verify=False):
    
    #load images for target
    image_links = []

    folder = data_container+'index-'+str(target)
    files = [f for f in os.walk(folder)]
    for f in files[0][2]:
        if 'stellar' not in f and 'directory' not in f:
            image_links.append(folder+'/'+f)
    
    with open(folder+'/stellar_coordinates.txt','rb') as f:
        data = f.readlines()
        ra = data[1][3:-1]
        dec = data[2][4:]

    arrays = []

    for link in image_links:
        inhdulist = pyfits.open(link)
        image_data = inhdulist[0].data
        if 'DSS' in link:
            new_image_data = lingray(image_data,'DSS')
            survey = 'DSS'
        else:
            new_image_data = loggray(image_data)
            if '2MASS' in link:
                survey = '2MASS'
            else:
                survey = 'WISE'
        arrays.append((new_image_data,link,survey))
        inhdulist.close()

    output = ([['Image Address','Target Index','Target Right Ascension','Target Declination','Survey','Band','Number of Central Blobs','Main Blob Center','Main Blob Radius',
        'Main Blob Displacement','Percent Outside Diffraction','Threshold Value','Percent of Image White','Validation','Error']])


    for array in arrays:
        img = array[0]
        title = array[1]
        survey = array[2]
        
        result = [title,target,ra,dec,survey,title.split('--')[1]]

        center = round(len(img)/2.)
        num_rows = len(img)
        num_cols = len(img[0])

        if img==None:
            result.extend(['NULL','NULL','NULL','NULL','NULL','NULL','NULL',0,'Image does not exist'])
            output.append(result)
            continue

        #throws out images where data has NaN errors
        if np.isnan(img).any():
            result.extend(['NULL','NULL','NULL','NULL','NULL','NULL','NULL',0,'Image has NaN pixel errors'])
            output.append(result)
            continue

        diffraction_points = diffract(img)

        if survey == '2MASS':
            blobs = blobh(img)
        else:
            blobs = blobl(img,survey)

        #Number of Central Blobs
        central = {}
        for blob in blobs:
            if blob in diffraction_points:
                central[blob] = blobs[blob]
        num_central = len(central)
        result.append(num_central)
        if not num_central:
            result.extend(['NULL','NULL','NULL','NULL'])
        else:
            #Main Blob Identification
            main_row = center
            main_col = center
            distance = 100
            main_rad = 0
            for (x,y) in blobs:
                d = sqrt((x-center)**2 + (y-center)**2)
                if d < distance:
                    distance = d
                    main_row = x
                    main_col = y
                    main_rad = blobs[(x,y)]
            result.extend([(main_row,main_col),main_rad,distance])

            #Percent Outside Diffraction
            altered = threshold(img)[0]
            main_region = circle_points(central[(main_row,main_col)],(main_row,main_col))[1]
            for blob in blobs:
                if blob != (main_row, main_col):
                    blob_points = circle_points(blobs[blob],blob)[1]
                    for (x,y) in blob_points:
                        if (x,y) not in main_region and y < num_rows and x < num_cols:
                            altered[y][x] = False          

            main_large = circle_points(int(round(1.25*main_rad)),(main_row,main_col))[1]
            inside = 0
            outside = 0
            for (row,col) in main_large:
                if row >= num_rows or col >= num_cols:
                    continue
                if altered[row][col]:
                    if (row,col) not in diffraction_points:
                        outside += 1
                    else:
                        inside += 1
            try:
                result.append(float(outside)/(inside+outside))
            except ZeroDivisionError:
                result.append(0.0)

        #Threshold Value
        thresh_results = threshold(img)
        thresh = thresh_results[1]
        if survey == 'DSS':
            result.append(float(thresh/255.))
        else:
            result.append(thresh)

        #Percent of Image White
        #over .5 correlates with bad candidate in w3, w4 bands
        num_pix = num_rows*num_cols
        white = 0
        for row in thresh_results[0]:
            for col in row:
                if col:
                    white += 1
        result.append(float(white)/num_pix)

        #Visual Check & Error Messages

        if num_central:
            if verify:
                plt.draw()
                plt.close()

                diffract(img)
                plt.title(title)
                plt.draw()
                plt.pause(.01)
                result.append(raw_input('Visual Verification? '))
                plt.close()
            else:
                result.append('')
            result.append('NULL')

        else:
            result.append(0)
            result.append('Image lacks central blob')
        output.append(result)

    return output



