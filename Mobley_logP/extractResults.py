# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# Fall 2015
# Adapted from Partition Coefficient project in Summer/Fall 2015 to extract results from Kalli Burley's SAMPL5 simulations

import numpy as np
import commands
import sys
import pickle as p
import os

database = p.load(open("updatedsmiles.p","rb"))
Warning_Limit = 3
kB = 1.380648*6.02214129/1000.0
conv = 4.184
warnings = []
results_Folder = "AllXVG/%s_%s/"
result_File = "AllXVG/%s_%s/results.pickle"

#cyc = "/work/cluster/burleyk/RotationProject/SAMPL_Data_Fall2015/Results/results_C6_%s.pickle"
cyc = "./AllResults/results_C6_%s.pickle"
#h2o = "/work/cluster/burleyk/RotationProject/SAMPL_Data_Fall2015/Results/results_H20_%s.pickle"
h2o = "./AllResults/results_H20_%s.pickle"
solvent_list = ['cyclohexane','water']


def getEnergy(fileName, Warning_Limit = 2.):
    warn = None
    if not os.path.isfile(fileName):
        split = fileName.split('/')
        print "\t file not found for", split[1], " in ", split[2], fileName
        warn = "File not found" 
        return None, None, warn

    getData = p.load(open(fileName, 'rb'))
    T = getData.temperature

    dF = getData.dFs[2]
    ddF = getData.ddFs[2]

    energies = np.array([e for (k, e) in dF.items()])
    uncertanties = np.array([e for (k, e) in ddF.items()])

    MBAR = np.array([dF['MBAR'], ddF['MBAR']])
        
    maxDif = max(energies) - min(energies)
    maxUn = max(uncertanties)
    tol = maxUn*Warning_Limit
    if (np.abs(maxDif) > (tol)) and (tol > 1):
        warn = "Warning energy difference (%.3f) is bigger than %s * the largest uncertainty (%.3f)" % (maxDif, str(Warning_Limit), maxUn)

    kJ = MBAR * kB * T
    return kJ[0],kJ[1],warn

for (num, entry) in database.items():
    En, Un, warn = getEnergy(cyc % num) 
    entry['cyclohexane'] = [En, Un]
    En, Un, warn = getEnergy(h2o % num)
    entry['water'] = [En, Un]

    Dif = np.array([(entry['cyclohexane'][0] - entry['water'][0]), np.sqrt(entry['water'][1]**2 + entry['cyclohexane'][1]**2)])
    LogP = Dif/(np.log(10.)*kB*298.15)
    entry['LogD_calc'] = LogP
    
p.dump(database, open('dictionary_allResults.p','wb'))
