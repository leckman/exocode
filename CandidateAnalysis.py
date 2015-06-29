'''
Find statistics of the candidates' properties and display results

Tam Nguyen 04/2015

'''

'''
Compile table of good candidates with all parameters
'''
import csv
import matplotlib.pyplot as plt
import math
import numpy as np


with open('Results/ConfirmedExoplanets/Candidates.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    table_candidates = [[e for e in r] for r in reader] 

objName = []
objNum = []
for i in range(len(table_candidates)):
    objNum.append(int(table_candidates[i][0]))
    objName.append(table_candidates[i][1])

with open('DataSets/Full Tables/IPAC_star.csv', 'r') as csvfile:
    reader1 = csv.reader(csvfile)
    table_star = [[e for e in r] for r in reader1] 
'''
Properties of all planet-host stars
'''
Teff_all =[]
Npl_all =[]
Mst_all = []
Rst_all = []
Vst_all = [] 
Dis_all = []

for i in range(len(table_star)-1):
    temp_all = table_star[i+1][16]
    if temp_all !='':
        Teff_all.append(float(temp_all))
        
    Npl_all.append(int(table_star[i+1][2]))
    
    mass = table_star[i+1][22]
    if mass !='':
        Mst_all.append(float(mass))
    
    vj = table_star[i+1][12]
    if vj !='':
        Vst_all.append(float(vj))
    
    radius = table_star[i+1][28]
    if radius!='':
        Rst_all.append(float(radius))
        
    dist = table_star[i+1][7]
    if dist!='':
        Dis_all.append(float(dist))

'''
Candidates properties
'''

Teff =[]
Npl =[]
Mst = []
Rst = []
Vst = []
Dis = []
for i in range(len(objNum)):
    temp = table_star[objNum[i]+1][16]
    if temp !='':
        Teff.append(float(temp))
#    else:
#        Teff.append(float('nan'))
    
    Npl.append(int(table_star[objNum[i]+1][2]))
    
    mass = table_star[objNum[i]+1][22]
    if mass !='':
        Mst.append(float(mass))
    
    vj = table_star[objNum[i]+1][12]
    if vj !='':
        Vst.append(float(vj))
    
    radius = table_star[objNum[i]+1][28]
    if radius!='':
        Rst.append(float(radius))
    
    dist = table_star[objNum[i]+1][7]
    if dist!='':
        Dis.append(float(dist))
    


'''
Convert temperature to spectral radiance at 22 um using Planck's law 
'''
h = 6.62606957e-34 # Planck constant [m^2 kg/s]
c = 299792458 # Speed of light [m/s]
k = 1.3806488e-23 #Boltzmann constant [m^2 kg s^-2 K^-1]
l=22e-6 # wavelength [m]
nu = c/l

Irad = []
for temp in Teff:
    T=temp
    Irad.append(2*h*pow(nu,3)/(pow(c,2) * math.exp(h*nu/(k*T)) - 1))
    
Irad_all = []
for temp in Teff_all:
    T=temp
    Irad_all.append(2*h*pow(nu,3)/(pow(c,2) * math.exp(h*nu/(k*T)) - 1))
    
#plt.figure()
#plt.hist(Irad)
#plt.xlabel('Spectral radiance at 22 um')

'''
Plot
'''
fig, ax = plt.subplots(3, 2,figsize=(15, 15))
ax[0][0].hist(Npl,normed=True,bins=range(1,7))
ax[0][0].hist(Npl_all,normed=True,alpha=0.5,color='red',bins=range(1,7))
ax[0][0].set_title('Number of planets',fontsize=17)
ax[0][0].tick_params(axis='both', which='major', labelsize=17)
ax[0][0].legend(["Candidates","All"])
ax[0][1].hist(Mst,normed=True,bins=np.linspace(0,3.5,11))
ax[0][1].hist(Mst_all,normed=True,alpha=0.5,color='red',bins=np.linspace(0,3.5,11))
ax[0][1].set_title('Star mass (solar mass)',fontsize=17)
ax[0][1].tick_params(axis='both', which='major', labelsize=17)
ax[0][1].legend(["Candidates","All"])
ax[1][0].hist(Rst,normed=True,bins=np.linspace(0,60,11))
ax[1][0].hist(Rst_all,normed=True,alpha=0.5,color='red',bins=np.linspace(0,60,11))
ax[1][0].set_title('Star radius (solar radius)',fontsize=17)
ax[1][0].tick_params(axis='both', which='major', labelsize=17)
ax[1][0].legend(["Candidates","All"])
ax[1][1].hist(Vst,normed=True,bins=np.linspace(0,25,11))
ax[1][1].hist(Vst_all,normed=True,alpha=0.5,color='red',bins=np.linspace(0,25,11))
ax[1][1].set_title('V-band brightness',fontsize=17)
ax[1][1].tick_params(axis='both', which='major', labelsize=17)
ax[1][1].legend(["Candidates","All"])
ax[2][0].hist(Teff,normed=True,bins=np.linspace(0,15000,21))
ax[2][0].hist(Teff_all,normed=True,alpha=0.5,color='red',bins=np.linspace(0,15000,21))
ax[2][0].set_title('Temperature (K)',fontsize=17)
ax[2][0].tick_params(axis='both', which='major', labelsize=13)
ax[2][0].legend(["Candidates","All"])
ax[2][1].hist(Dis,normed=True,bins=np.linspace(0,2500,11))
ax[2][1].hist(Dis_all,normed=True,alpha=0.5,color='red',bins=np.linspace(0,2500,11))
ax[2][1].set_title('Distance (pc)',fontsize=17)
ax[2][1].tick_params(axis='both', which='major', labelsize=17)
ax[2][1].legend(["Candidates","All"])

fig.tight_layout()
#plt.savefig('DataAnalysis.jpg')