'''
Use FinderChart to acquire images of given stars from 2MASS, DSS, and WISE surveys
irsa.ipac.caltech.edu/onlinehelp/Finderchart/#id=api
http://irsa.ipac.caltech.edu/docs/program_interface/api_images.html
Limited to 1000 sources per search

Laura Eckman 12-06-2015
'''

import csv
import os
import xml.etree.ElementTree as ET
import urllib2

### EDITABLE ###############################################################################

download_catalog = 'Catalogs/random_catalog_sample+1000.csv' #catalog of targets
max_indices = int(download_catalog.split('+')[1][:-4]) #maximum index to download (set to all)
data_container = 'FITS/RandSample-1000/' #containing folder for each target's image set

############################################################################################

with open(download_catalog,'rb') as csvfile: #rand cat
    reader = csv.reader(csvfile)
    table = [[e for e in r] for r in reader]

#table row fmt:
#ra,dec (degree measurements as strings)  

size = 1.0 #arcmin

for i in range(max_indices):
    folder = containing_folder+'index-'+str(i) #rand cat
    if not os.path.exists(folder):
        os.makedirs(folder)
    fileList = os.listdir(folder);

    if len(fileList)==0:
        print i
        ra = float(table[i][0])
        dec = float(table[i][1])
        
        position = open(folder+'/stellar_coordinates.txt','wb')
        position.write('Target is row '+str(i)+' of file random_catalog_sample+1000.csv\n')
        position.write('ra '+str(ra)+'\n')
        position.write('dec '+str(dec))
        position.close()
       
        #FinderChart url generation
        base = 'http://irsa.ipac.caltech.edu/applications/finderchart/servlet/api?'
        locstr = 'locstr='+str(ra)+'+'+str(dec)+'+Equatorial+J2000'
        surveys = '&survey=DSS&survey=2MASS&survey=WISE'
        slicing = '&subsetsize='+str(size)
        orient = '&orientation=left' #default
        reproject = '&reproject=false' #default
        grid = '&grid=false' #default
        marker = '&marker=false' #default
        full_url = base+locstr+surveys+slicing+orient+reproject+grid+marker

        f = urllib2.urlopen(full_url)
        xml_file = f.read() #returns xml FinderChart file as string

        imgfmt = 'fits' #'jpg' format actually saves as png, badly named api property
        root = ET.fromstring(xml_file) #turns xml_file into hierarchical element structure
        result = root[1]
        for image in result.findall('image'):
            surveyname = image[0].text.replace(' ','+')
            band = image[1].text.replace(' ','+')
            img_link = image.find(imgfmt+'url').text #url of image
            dwnld_file = surveyname+"--"+band #filename

            img = open(folder+'/'+dwnld_file,'wb')
            img.write(urllib2.urlopen(img_link).read())
            img.close

                
