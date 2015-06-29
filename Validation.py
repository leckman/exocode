'''
Display images of a number of targets for visual validation. ImgProcessing.py needs to be run before to get y_pred_test. 

Tam Nguyen 04/2015
'''

import pyfits
import matplotlib.pyplot as plt
import os

# Define parameters
L_ang=0.8;  #arcmin

# Circle radius
l=22e-6 #m
D = 0.4 #m
R_ang = (1.22*l/D)*180/3.14*60 #arcmin
    
for n in range(250): # input range of interest here

    #########################################################################
    '''
    Load images queried from IRSA within region of interest
    '''
    
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
        ax1.set_title('WISE #1')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax1.add_patch(circle)
        ax1.scatter([cen], [cen], marker='+')
        ax1.text(-15,20,str(n))
        
        ax2.imshow(im[4*i+1], cmap=plt.cm.gray)
        ax2.axis('off')
        ax2.set_title('WISE #2')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax2.add_patch(circle)
        ax2.scatter([cen], [cen], marker='+')
        
        ax3.imshow(im[4*i+2], cmap=plt.cm.gray)
        ax3.axis('off')
        ax3.set_title('WISE #3')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax3.add_patch(circle)
        ax3.scatter([cen], [cen], marker='+')
        
        ax4.imshow(im[4*i+3], cmap=plt.cm.gray)
        ax4.axis('off')
        ax4.set_title('WISE #4')
        circle = plt.Circle((cen, cen), R_pix, color='lime', linewidth=2, fill=False)
        ax4.add_patch(circle)
        ax4.scatter([cen], [cen], marker='+') 
        if y_pred_test[n] == 1:
            ax4.text(40, 20, 'GOOD',color = 'blue')
        else:
            ax4.text(40, 20, 'BAD',color = 'red')
        
        
        
    
    #########################################################################
    '''
    Plot raw image
    '''
        
    fig1, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(7, 2))
    PlotImages(images,fig1,ax1, ax2, ax3, ax4)
    plt.savefig('Validation/Validation_1/validation'+str(n)+'.jpg')
      
