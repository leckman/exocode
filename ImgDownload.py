'''
Check folders to see if images were downloaded correctly from server. Input/Output folders can be changed to run the data set of interests. 

Tam Nguyen 03/2015
'''
import csv
import subprocess
import os
from astropy.io.votable import parse_single_table

# Input/output parameters
size="0.8arcmin"
folderO = 'Images'
folderI = 'VOTable/IPAC'
filename = 'IPAC_reduced' 
destination = 'IPAC'


# Get images
def getImages(ra,dec,size,n):
    dirIn = folderI + "/" + str(n)
    for file in os.listdir(dirIn):
        table = parse_single_table(dirIn+'/'+file).to_table()
        Nrow = len(table)
        for row in range(Nrow):
            url = table[row]['sia_url']
            process=subprocess.Popen(["wget" ,"-P", folderO+'/'+destination+'/'+str(n), url+'?center='+str(ra)+','+str(dec)+'^&size='+size],
                             shell=True,
                             close_fds=True)
            process.wait()

# Open csv file            
with open('DataSets/'+filename+'.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    table = [[e for e in r] for r in reader] 

# Check 
k = 1
while k<2:
    for i in range(1000,1127): # input range of interest here
            dir = folderO+'/'+destination+'/'+str(i)
            if not os.path.exists(dir):
                os.makedirs(dir)
            fileList = os.listdir(dir);
            for file in fileList:
                lastchar = file[len(file)-1]
                if lastchar.isdigit()==True:
                    print file
                    os.remove(dir+'/'+file)
            if len(os.listdir(dir))<4:
                print str(i) + ": not enough"
                ra = table[i][1]   
                dec = table[i][2]
                getImages(ra,dec,size,i) 
                print "re-queried"
            elif len(os.listdir(dir))>4:
                print str(i) + ": too many" 
                fsizeMax = 0
                fMax = 0
                fileList = os.listdir(dir);
                for f in fileList:
                    fsize = os.stat(dir+'/'+f).st_size
                    if fsize > fsizeMax:
                        fsizeMax = fsize
                        fMax = f
                for f in fileList:
                    if f[0:7] != fMax[0:7]:
                        print f
                        os.remove(dir+"/"+f)
            else:
                print str(i) + ": all images are downloaded correctly"
    k+=1

 
             
 
         
        
