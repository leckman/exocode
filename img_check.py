import os
from tabulate import tabulate

files = sorted(['2MASS--J','2MASS--K','2MASS--H','DSS--DSS1+Blue','DSS--DSS1+Red','DSS--DSS2+Blue','DSS--DSS2+IR','DSS--DSS2+Red','WISE+(AllWISE)--w1','WISE+(AllWISE)--w2','WISE+(AllWISE)--w3','WISE+(AllWISE)--w4'])
missing = {}
for i in files:
    missing[i] = []
image_list = []
dir = 'RandSample/'
RandSample = [f for f in os.walk(dir)]
folders = sorted([dir+index for index in RandSample[0][1]])
folders.remove(dir+'FITS')
inventory= [[i for i in files]]
inventory[0].append('FOLDER')
for folder in folders:
    img_files = [i[2] for i in os.walk(folder)]
    new_row = [i in img_files[0] for i in files]
    new_row.append(folder)
    with open(folder+'/file_directory','wb') as k:
        k.write('Available files:\n\n')
        for i in range(len(files)):
            k.write(files[i]+': '+str(new_row[i])+'\n')
        for i in range(len(new_row)):
            if not new_row[i]:
                k.write('\nMISSING '+files[i])
                missing[files[i]].append(folder)
    inventory.append(new_row)

with open('missing_files.txt','wb') as k:
    k.write('MISSING FILES:\n\n')
    for elt in missing:
       k.write(elt+': '+str(missing[elt])+'\n')
       k.write('    Num missing: '+str(len(missing[elt]))+'\n')



