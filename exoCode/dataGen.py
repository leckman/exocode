import time
import csv 
from analysis_script import target_analysis


#### EDITABLE ##################################################################################

data_container = 'FITS/RandSample-2000/' #alter to analyze a different set

min_index = 0
max_index = int(data_container.split('-')[1][:-1]) #alter to analyze only a subset

output_file = 'Results/RandSample_2000/ANALYSIS.csv' #make sure this file path actually exists!

################################################################################################

t = time.time()
full = target_analysis(min_index,data_container)

for target in range (min_index+1,max_index):
    k = target_analysis(target,data_container)
    full.extend(k[1:])

print time.time()-t, 'SECONDS'

with open(output_file,'wb') as f:
    writer = csv.writer(f)
    writer.writerows(full)

print 'COMPLETE'
