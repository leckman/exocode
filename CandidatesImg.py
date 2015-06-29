'''
Display images of all candidates found

Tam Nguyen 04/2015
'''
import csv
import os
import pyfits
import matplotlib.pyplot as plt

with open('Results/ConfirmedExoplanets/Candidates.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    table_candidates = [[e for e in r] for r in reader] 

objName = []
objNum = []
for i in range(len(table_candidates)):
    objNum.append(int(table_candidates[i][0]))
    objName.append(table_candidates[i][1])

#########################################################################
'''
Load images queried from IRSA within region of interest
'''
# Define parameters
L_ang=0.8;  #arcmin

# Circle radius
l=22e-6 #m
D = 0.4 #m
R_ang = (1.22*l/D)*180/3.14*60 #arcmin

for i in range(len(objNum))  :
    n=objNum[i]
    images = []
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
        ax1.text(8,45,'WISE #1')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax1.add_patch(circle)
        ax1.scatter([cen], [cen], marker='+')
        ax1.text(-15,20,str(n))
        
        ax2.imshow(im[4*i+1], cmap=plt.cm.gray)
        ax2.axis('off')
        ax2.text(8,45,'WISE #2')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax2.add_patch(circle)
        ax2.scatter([cen], [cen], marker='+')
        
        ax3.imshow(im[4*i+2], cmap=plt.cm.gray)
        ax3.axis('off')
        ax3.text(8,45,'WISE #3')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax3.add_patch(circle)
        ax3.scatter([cen], [cen], marker='+')
        
        ax4.imshow(im[4*i+3], cmap=plt.cm.gray)
        ax4.axis('off')
        ax4.text(8,45,'WISE #4')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax4.add_patch(circle)
        ax4.scatter([cen], [cen], marker='+') 

    #########################################################################
    '''
    Plot raw image
    '''
        
    fig1, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(7, 2))
    PlotImages(images,fig1,ax1, ax2, ax3, ax4)
    plt.suptitle(objName[i])
    plt.savefig('Validation/Candidates/candidate'+str(n)+'.jpg')
      
