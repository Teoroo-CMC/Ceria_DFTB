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

spl_new=np.loadtxt('Ce-O.spl',skiprows=3,usecols=[0,2])
plt.title("Repulsive potential")
plt.xlabel("Distance (Bohr)")
plt.ylabel("Energy (Hartree)")
plt.xlim(3,10)
plt.ylim(0,0.05)
plt.plot(spl_new[:,0],spl_new[:,1],'--',color="black")
plt.show()

