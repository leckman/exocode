'''
Creates a random sampling of the full tycho_2mass_wise_XMATCH-POS.csv target catalog

Laura Eckman 15/06/2015
'''

import csv
import random as rand

with open('Catalogs/tycho_2mass_wise_XMATCH-POS.csv','rb') as csvf:
    reader = csv.reader(csvf)
    table = [r for r in reader]

desired_rows = 2000
rand_index = []

for r in range(desired_rows):
    k = rand.randint(1,len(table))
    while k in rand_index: #prevents duplicates
        k = rand.randint(1,len(table))
    rand_index.append(k)

output_name = 'Catalogs/random_catalog_sample+'+str(desired_rows)
with open(output_name+'.csv','wb') as outf:
    writer = csv.writer(outf)
    writer.writerows([table[x] for x in rand_index])

print 'Download complete to: '+output_name+'.csv'
