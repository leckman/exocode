'''
Creates a random sampling of the full tycho_2mass_wise_XMATCH-POS.csv target catalog

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
