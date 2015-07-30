'''
Checks for proper download of images, leaves result txt file in each target index folder
Already run for RandSample-2000

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

import os
from tabulate import tabulate

files = sorted(['2MASS--J','2MASS--K','2MASS--H','DSS--DSS1+Blue','DSS--DSS1+Red','DSS--DSS2+Blue','DSS--DSS2+IR','DSS--DSS2+Red','WISE+(AllWISE)--w1','WISE+(AllWISE)--w2','WISE+(AllWISE)--w3','WISE+(AllWISE)--w4'])
missing = {}
for i in files:
    missing[i] = []
image_list = []
directory = 'FITS/'####+'/'
RandSample = [f for f in os.walk(directory)]
folders = sorted([directory+index for index in RandSample[0][1]])
inventory= [[i for i in files]]
inventory[0].append('FOLDER')
for folder in folders:
    img_files = [i[2] for i in os.walk(folder)]
    new_row = [i in img_files[0] for i in files]
    new_row.append(folder)
    with open(folder+'/file_directory.txt','wb') as k:
        k.write('Available files:\n\n')
        for i in range(len(files)):
            k.write(files[i]+': '+str(new_row[i])+'\n')
        for i in range(len(new_row)):
            if not new_row[i]:
                k.write('\nMISSING '+files[i])
                missing[files[i]].append(folder)
    inventory.append(new_row)





