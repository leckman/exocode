'''
Creates a txt list of good candidates based on visual validation following
preprocessing from data

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

import csv
import pyfits
from matplotlib import pyplot as plt
from array_processing import loggray
from diffraction import diffract

#constants equating different values to their indices in data lists
address = 0
index = 1
ra = 2
dec = 3
survey = 4
band = 5
num_blobs = 6
center = 7
radius = 8
displacement = 9
diffraction = 10
thresh = 11
white = 12
validation = 13
error = 14

candidates = []

f = open('Results/RandSample_2000/ANALYSIS.csv','rb')
data = csv.reader(f)
for row in data:
    if row[band] == 'w3' and row[error] == 'NULL':
        link = row[address][:-1] + '4'
        inhdulist = pyfits.open(link)
        image_data = inhdulist[0].data
        new_image_data = loggray(image_data)
        inhdulist.close()

        diffract(new_image_data)
        plt.draw()
        plt.pause(.1)
        good = int(raw_input('Good? '))
        if good:
            candidates.append(row[index])
        plt.close()

with open('Results/RandSample_2000/good_candidates_from_w3.txt','wb') as k:
    k.write('Good Candidate Index Numbers')
    for target in candidates:
        k.write('\n'+target)
