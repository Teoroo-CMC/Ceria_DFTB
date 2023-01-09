import numpy as np
import yaml
import matplotlib.pyplot as plt
import pandas as pd
import copy
import math
import os

plt.rcParams['axes.linewidth'] = 2
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = "large"
plt.rcParams['ytick.labelsize'] = "large"

with open(r'band_VASP.yaml') as file:
    band=pd.json_normalize(yaml.load(file,Loader=yaml.SafeLoader) )

with open(r'band.yaml') as file:
    band_DFTB=pd.json_normalize(yaml.load(file,Loader=yaml.SafeLoader) )

tmp=band['phonon']
d=[]
f=[]
for t in tmp:
    for tt in t:
        d.append(tt['distance'])
        fs=[]
        for ttt in tt['band']:
            fs.append(ttt['frequency'])
        f.append(fs)
        
tmp=band_DFTB['phonon']
d_DFTB=[]
f_DFTB=[]
for t in tmp:
    for tt in t:
        d_DFTB.append(tt['distance']*1.89)
        fs=[]
        for ttt in tt['band']:
            fs.append(ttt['frequency'])
        f_DFTB.append(fs)
plt.title("Phonon bandstructure \n BLACK: VASP      RED: DFTB+")
#plt.text(0.01,18.5,"BLACK: VASP, RED: DFTB+",size='x-large')

xpos=1.8897259886*np.array([0.0, 0.0679357, 0.1511397, 0.2472153,0.2952531,0.3292209 ])

plt.xticks(xpos,['W','L','$\Gamma$','X','W','K'])
plt.vlines(xpos,0.0,20.0,color='black',linestyles='solid')
plt.xlim(min(xpos),max(xpos))
plt.ylim(0.0,20.0)
plt.xlabel('Wave vector')
plt.ylabel('Frequency (THz)')
plt.plot(d,f, '-', color='black',label='VASP')
plt.plot(d_DFTB,f_DFTB, '--', color='red',label='DFTB')
plt.show()

