# ExoCode #

Generates .csv files including data on the existence of various features of interest 
from the Digitized Sky Survey (DSS), 2-micron All Sky Survey (2MASS), and 
Wide-field Infrared Survey Explorer (WISE) image catalogs. The goal is to use the 
data to identify candidates that might have circumstellar debris disks. 

---------------

TO USE:
* Use dataAcq.py to retrieve the images for one of the provided catalogs in  Catalogs/
* * You can also use one of your own, provided the format remains the same: ra,dec (degrees)
*  Use dataGen.py to run analysis on the downloaded images and output the results to a new .csv

You should only have to touch the offset code at the top of each program (denoted 'EDITABLE')
to accomplish your analysis

Run Guidelines:
*Assumes data_container variables in each script are equivalent*

Command line: (in exoCode containing directory)
    cd exoCode
    python dataAcq.py
    python dataGen.py

In python:

```
#!python

from exoCode import dataAcq
from exoCode import dataGen
```