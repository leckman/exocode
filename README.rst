**ExoCode**

Generates .csv files including data on the existence of various features of interest 
from the Digitized Sky Survey (DSS), 2-micron All Sky Survey (2MASS), and 
Wide-field Infrared Survey Explorer (WISE) image catalogs. The goal is to use the 
data to identify candidates that might have circumstellar debris disks. 

This release (1.2.0) includes catalogs tycho_2mass_wise-XMATCH-POS.csv (full catalog), RandSample+1000.csv,
RandSample+2000.csv, and tam_cat_sample.csv. Pre-downloaded images from tam_cat_sample.csv are available
for your convenience in FITS/Tam/. All other catalogs must first have images downloaded to be useful.

See **CHANGES.txt** for more detailed updates with this release.

Dependent on scikit-image (skimage), matplotlib, numpy, and astropy. 

Lives at https://bitbucket.org/leckman/exoplanets/overview

---------------

**TO USE:**

* Use dataAcq.py to retrieve the images for one of the provided catalogs in  Catalogs/

  * You can also use one of your own, provided the format remains the same: ra,dec (degrees)

  * Data included for tam_cat_sample.csv catalog under FITS/TAM/

*  Use dataGen.py to run analysis on the downloaded images and output the results to a new .csv

**Run Guidelines:**

Command line: (in containing directory)

    cd src

    python dataGen.py

In python:

    import src.dataGen

**New Graphical Interface**

* run application

* select desired catalog

* follow prompts to gather data, flip through indices, display images

* can be run using $ ./GUI.sh in src directory

  * alternatively, use $ python GUI.py


**Full Documentation:** https://docs.google.com/document/d/1-QtbvASw43S03IHlEPk4qlstk8aNtAmu8uT2uNk6otY/edit?usp=sharing 
