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
