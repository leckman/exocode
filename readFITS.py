'''
Read FITS file and implement image processing. This is mostly used for single target validation. 

Tam Nguyen 02/2015
'''
import pyfits
import matplotlib.pyplot as plt
import numpy as np


#########################################################################
'''
Load images queried from IRSA within region of interest
'''
import os
images = []
n=100
dir = "Images/IPAC/"+str(n)
for file in os.listdir(dir):
    #hdulist = pyfits.open(file)
    print file
    img = pyfits.getdata(dir + '/'+ file)
    images.append(img)
    
########################################################################
'''
Compute location and size of diffraction scale circle
'''
# Size of image
L = len(images[0]) #pixels
L_ang=0.8;  #arcmin

# Circle radius
l=22e-6 #m
D = 0.4 #m
R_ang = (1.22*l/D)*180/3.14*60 #arcmin
R_pix = R_ang/L_ang*L

# Center
cen = round(L/2)


#########################################################################
''' 
Define plot function 
'''

def PlotImages(im,fig,ax1,ax2,ax3,ax4):  
    i = 0
    
    ax1.imshow(im[4*i], cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('WISE 1 (3.4 um)')
#    circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
#    ax1.add_patch(circle)
    ax1.scatter([cen], [cen], marker='+')
    ax1.text(-15,20,str(n))

    
    ax2.imshow(im[4*i+1], cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('WISE 2 (4.6 um)')
#    circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
#    ax2.add_patch(circle)
    ax2.scatter([cen], [cen], marker='+')
    
    ax3.imshow(im[4*i+2], cmap=plt.cm.gray)
    ax3.axis('off')
    ax3.set_title('WISE 3 (12 um)')
#    circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
#    ax3.add_patch(circle)
    ax3.scatter([cen], [cen], marker='+')
    
    ax4.imshow(im[4*i+3], cmap=plt.cm.gray)
    ax4.axis('off')
    ax4.set_title('WISE 4 (22 um)')
#    circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
#    ax4.add_patch(circle)
    ax4.scatter([cen], [cen], marker='+') 
    
    fig.tight_layout()

#########################################################################
'''
Plot raw image
'''
    
fig1, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(9, 3))
PlotImages(images,fig1,ax1, ax2, ax3, ax4)
  
plt.savefig('sample.png')
#########################################################################
'''
Threshold
'''
from skimage.filter import threshold_otsu

binary=[]
im_thres=[]
for i in range(len(images)):
    thres = threshold_otsu(images[i])
    bin = 1*(images[i] > thres)
    binary.append(bin)
    Ithres = np.multiply(bin,images[i])
    im_thres.append(Ithres)

fig2, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(9, 3))
PlotImages(im_thres,fig2,ax1, ax2, ax3, ax4)
plt.savefig('sample_thres')

# make copy of im_thres
im_pr = []
for i in range(len(im_thres)):
    a = np.empty_like(im_thres[i])
    a[:] = im_thres[i]
    im_pr.append(a)


'''
Blob detection
'''
from skimage.feature import blob_log
from math import sqrt,pow

#im_blob=[]
margin = 1.5
for i in range(len(images)):
    image = im_pr[i]
    blobs = blob_log(image, max_sigma=10,num_sigma=10)

    if len(blobs) > 0:
        blobs[:, 2] = blobs[:, 2] * sqrt(2) * margin 
        
#        fig, ax = plt.subplots(1, 1)
#        ax.imshow(image, interpolation='nearest')
#        for blob in blobs:
#            y, x, r = blob
#            c = plt.Circle((x, y), r, linewidth=2, fill=False)
#            ax.add_patch(c)
#    
#        plt.show()
    
#    if len(blobs)>1:
#        Iblob_c=[]
#        for i in range(len(blobs)):
#            x,y,r = blobs[i]
#            if cen>x-r and cen<x+r and cen<y+r and cen>y-r:
#                Iblob_c.append(i)
#            
#        if len(Iblob_c)>0:
#            blobs_extra = np.delete(blobs,Iblob_c,0)
        blobs_extra=[]
        for blob in blobs:
            x,y,r = blob
#            if cen<x-r and cen>x+r and cen>y+r and cen<y-r:
            if pow(x-cen,2)+pow(y-cen,2)>pow(r+R_pix,2):
                blobs_extra.append(blob)
            
    #        print blobs_extra
            for blob in blobs_extra:
                x,y,r = blob
#                print[x,y,r]
                kr_min = max(x-r,0);
                kr_max = min(x+r,image.shape[0]);
                lr_min = max(y-r,0);
                lr_max = min(y+r,image.shape[1]);
                for k in range(kr_min,kr_max):
                    for l in range(lr_min,lr_max):
                        if pow(k-x,2)+pow(l-y,2)<pow(r,2):
                            image[k][l]=0



#########################################################################
''' 
Compute centroid and percentage of spot outside of circle
'''
from math import sqrt


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
    if mass == 0:
        COM=[20,20] #arbitrarily large number
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
    if Stotal ==0:
        Per = 100
    else:
        Per = float(count)/Stotal*100
    OutofRange.append(Per)

## Plot results
default_font = {'fontname':'Arial', 'size':'15'}
fig2, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(9, 3))
PlotImages(im_pr,fig2,ax1, ax2, ax3, ax4)
ax1.text(0, 40, "err_c = "+str(round(CMerr[0],2)) + " pixels",default_font)
ax2.text(0, 40, "err_c = "+str(round(CMerr[1],2)) + " pixels",default_font)
ax3.text(0, 40, "err_c = "+str(round(CMerr[2],2)) + " pixels",default_font)
ax4.text(0, 40, "err_c = "+str(round(CMerr[3],2)) + " pixels",default_font)

ax1.text(0, 45, "extended by "+str(round(OutofRange[0],2)) + "%",default_font)
ax2.text(0, 45, "extended by "+str(round(OutofRange[1],2)) + "%",default_font)
ax3.text(0, 45, "extended by "+str(round(OutofRange[2],2)) + "%",default_font)
ax4.text(0, 45, "extended by "+str(round(OutofRange[3],2)) + "%",default_font)

circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
ax1.add_patch(circle)
circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
ax2.add_patch(circle)
circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
ax3.add_patch(circle)
circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
ax4.add_patch(circle)

plt.savefig('sample_processed.png')