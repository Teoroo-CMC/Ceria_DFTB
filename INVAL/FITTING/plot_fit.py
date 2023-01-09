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



CCS_error=np.loadtxt('CCS_error.out')
CCS_error[:,0]=3*CCS_error[:,0]/CCS_error[:,3]
CCS_error[:,1]=3*CCS_error[:,1]/CCS_error[:,3]
plt.figure(figsize=(5, 5))
#plt.title("Correlation plot")
plt.xlabel("Target repulsive energy (eV/FU)")
plt.ylabel("Fitted repulsive energy (eV/FU)")
plt.scatter(CCS_error[:,0],CCS_error[:,1],color='red')
plt.plot([min(CCS_error[:,1]),max(CCS_error[:,1])],[ min(CCS_error[:,1]),max(CCS_error[:,1]) ],'--',color='black'  )
plt.tight_layout()
plt.savefig("fit.png", dpi=1000)
plt.show()

