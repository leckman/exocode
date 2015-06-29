'''
This script loads both training and actual data sets, implement image processing, and select good candidates. 

Tam Nguyen 04/2015

'''
import pyfits
import numpy as np
from skimage.feature import blob_log
import math
from time import time
import matplotlib.pyplot as plt
from skimage.filter import threshold_otsu
from math import sqrt,pow

#################################################################################
'''
Constants
'''
L_ang=0.8;  #arcmin

# Circle radius
l=22e-6 #m
D = 0.4 #m
R_ang = (1.22*l/D)*180/3.14*60 #arcmin

#################################################################################
def ParamCalc(images,option):
    '''
    Compute location and size of diffraction scale circle
    '''
    # Size of image
    L = len(images[0]) #pixels
    R_pix = R_ang/L_ang*L
    
    # Center
    cen = round(L/2)
    
    '''
    Threshold
    '''
    binary=[]
    im_thres=[]
    for i in range(len(images)):
        thres = threshold_otsu(images[i])
        bin = 1*(images[i] > thres)
        binary.append(bin)
        Ithres = np.multiply(bin,images[i])
        im_thres.append(Ithres)
        
    '''
    Blob detection
    '''
    ############################################################
    if option == 0:
        im_pr = im_thres
    else:
        margin = 1.5
        for i in range(len(images)):
            image = im_thres[i]
#            thres = image.mean()
            blobs = blob_log(image, max_sigma=10,num_sigma=10)
            if len(blobs) > 0:
                blobs[:, 2] = blobs[:, 2] * sqrt(2) * margin 
            if len(blobs) < 2:
                im_pr = im_thres
            else:
                Iblob_c = []
                ############################################################    
                if option ==1:
                    r_off = []
                    for blob in blobs:
                        x,y,r = blob
                        r = sqrt(pow(x-cen,2)+pow(y-cen,2))
                        r_off.append(r)  
                    Iblob_c.append(np.argmin(r_off))
                ############################################################        
                if option ==2:
                    blobs_extra=[]
                    for blob in blobs:
                        x,y,r = blob
                        if pow(x-cen,2)+pow(y-cen,2)>pow(r+R_pix,2):
                            blobs_extra.append(blob)
                    for blob in blobs_extra:
                        x,y,r = blob
                        kr_min = max(x-r,0);
                        kr_max = min(x+r,image.shape[0]);
                        lr_min = max(y-r,0);
                        lr_max = min(y+r,image.shape[1]);
                        for k in range(kr_min,kr_max):
                            for l in range(lr_min,lr_max):
                                if pow(k-x,2)+pow(l-y,2)<pow(r,2):
                                    image[k][l]=0
            im_pr = im_thres    
                

    #################################################################################
    ''' 
    Compute centroid and percentage of spot outside of circle
    '''
    # Compute Centroid
    def COM(img):
        Mx = 0
        My = 0
        mass = 0
        
        for i in range(len(img)):
            for j in range (len(img[i])):
                if img[i][j]:
                    Mx+=j
                    My+=i
                    mass+=1
        if mass == 0 or math.isnan(mass)==True:
            COM=[len(img[i])/2,len(img[i])/2]
        else:
            COM = (float(Mx)/mass, float(My)/mass)
        return COM
    
    CMlist = []
    CMerr = []
    for i in range(len(im_pr)):
        CM = COM(im_pr[i])
        Err = sqrt(pow((CM[0]-cen),2) + pow((CM[1]-cen),2))
        CMlist.append(CM)
        CMerr.append(Err)
        
    # Compute percentage of spot outside of circle
    OutofRange=[]
    for i in range(len(im_pr)):
        count = 0
        nzlist = np.nonzero(im_pr[i])
        for k in range(len(nzlist[0])):
            x = nzlist[0][k]
            y = nzlist[1][k]
            r = sqrt(pow((x-cen),2)+ pow((y-cen),2))
            if r>R_pix:
                im_prr= im_pr[i]
                count +=im_prr[x][y]
        Stotal = float(np.sum(im_pr[i]))
        if Stotal ==0 or math.isnan(Stotal)==True:
            Per = 100
        else:
            Per = float(count)/float(np.sum(im_pr[i]))*100
        OutofRange.append(Per)
        
        
    CMerr_max = max(CMerr)
    OutofRange_max = max(OutofRange)
    
    result = [CMerr_max, OutofRange_max]
    
    return result
#################################################################################
'''
Load images queried from IRSA within region of interest and compute relevant parameters
'''
import os
option = 2
results = []

start_time = time()
for i in range(1127):
    images = []
    dir = "Images/IPAC/"+ str(i)
    for file in os.listdir(dir):
        #hdulist = pyfits.open(file)
        print file
        img = pyfits.getdata(dir + '/'+ file)
        images.append(img)
    res = ParamCalc(images,option)
    results.append(res)
end_time = time()
computation_time = end_time-start_time

# load good training set
results_good=[]
for i in range(113):
    images = []
    dir = "Images_training/CASLEO_new/"+ str(i)
    for file in os.listdir(dir):
        #hdulist = pyfits.open(file)
        print file
        img = pyfits.getdata(dir + '/'+ file)
        images.append(img)
    res = ParamCalc(images,option)
    results_good.append(res)

##################################################################################
'''
Compute and Plot results
'''
#import matplotlib.pyplot as plt

x=[]
y=[]
for i in range(len(results)):
    x.append(results[i][0])
    y.append(results[i][1])
    
x_good=[]
y_good=[]
for i in range(len(results_good)):
    x_good.append(results_good[i][0])
    y_good.append(results_good[i][1])
    

#plt.figure(figsize=(6,7))
#plt.scatter(x, y,s=50,c='b',alpha=0.5)
#plt.scatter(x_good, y_good,s=50,c='g',alpha=0.5)
#plt.xlabel('centroid displacement (pixel)',fontsize=15)
#plt.ylabel('percentage outside of diffraction-limit range (%)',fontsize=15)
#plt.grid()
#
#plt.show()

'''
Eliminate outliers in CASLEO data 
'''

# Remove outliers
results_training=[]
x_training=[]
y_training=[]
for i in range(len(results_good)):
    if results_good[i][1]<90 and results_good[i][0]<10:
        results_training.append(results_good[i])
        x_training.append(results_good[i][0])
        y_training.append(results_good[i][1])

x_training = np.asarray(x_training)
y_training = np.asarray(y_training)

x_1sig = np.mean(x_training)+np.std(x_training)
x_2sig = np.mean(x_training)+2*np.std(x_training)
x_3sig = np.mean(x_training)+3*np.std(x_training)
x_4sig = np.mean(x_training)+4*np.std(x_training)

y_1sig = np.mean(y_training)+np.std(y_training)
y_2sig = np.mean(y_training)+2*np.std(y_training)
y_3sig = np.mean(y_training)+3*np.std(y_training)
y_4sig = np.mean(y_training)+4*np.std(y_training)

x_max = x_4sig
y_max = y_4sig

y_pred_test=[]
for i in range(len(results)):
    pred = 1*(x[i]<x_max and y[i]<y_max);
    y_pred_test.append(pred)
y_pred_test = np.asarray(y_pred_test)

#'''
#Good candidate detection
#'''
n_candidates = y_pred_test[y_pred_test ==1].size
candidates = np.array(np.where(y_pred_test==1))
candidate_list = candidates.ravel()
'''
Look up names of candidates
'''
import csv
with open('DataSets/IPAC_reduced.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    table = [[e for e in r] for r in reader] 

#print "Good Candidates:"
for nstar in candidate_list:
    print str(nstar) + "," + str(table[nstar][0])+","+str(table[nstar][1])+","+str(table[nstar][2])+","+str(table[nstar][3])+","+str(table[nstar][4])
np.savetxt("results.csv", np.asarray(results), delimiter=",")

'''
Plot
'''
X_train = np.asarray(results_training)

fig = plt.figure(figsize=(6,7))
plt.scatter(X_train[:,0], X_train[:,1], c=[8.0/255.0,70.0/255.0,139.0/255.0],s=50)
#b2 = plt.scatter(X_test[:,0], X_test[:,1], c='yellow')
plt.xlabel('Centroid displacement (pixel)',fontsize=18)
plt.ylabel('Out of range (%)',fontsize=18)
plt.axis('tight')
#fig.patch.set_alpha(0)

axes = plt.gca()
axes.set_xlim([0,6])
axes.set_ylim([-0.1,15])
#axes.patch.set_facecolor([8.0/255.0,70.0/255.0,139.0/255.0])
plt.plot([0,x_1sig],[y_1sig,y_1sig],color=[0.4,0.1,0.1],linewidth = 3,linestyle='--')
plt.plot([x_1sig,x_1sig],[0,y_1sig],color=[0.4,0.1,0.1],linewidth = 3,linestyle='--')

plt.plot([0,x_2sig],[y_2sig,y_2sig],color=[0.6,0.1,0.1],linewidth = 3,linestyle='--')
plt.plot([x_2sig,x_2sig],[0,y_2sig],color=[0.6,0.1,0.1],linewidth = 3,linestyle='--')

plt.plot([0,x_3sig],[y_3sig,y_3sig],color=[0.8,0.1,0.1],linewidth = 3,linestyle='--')
plt.plot([x_3sig,x_3sig],[0,y_3sig],color=[0.8,0.1,0.1],linewidth = 3,linestyle='--')
plt.grid()

plt.plot([0,x_4sig],[y_4sig,y_4sig],color=[1.0,0.1,0.1],linewidth = 3,linestyle='--')
plt.plot([x_4sig,x_4sig],[0,y_4sig],color=[1.0,0.1,0.1],linewidth = 3,linestyle='--')
plt.grid()

plt.grid()
plt.show()