# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# Fall 2015
# Adapted to extract box size data

import numpy as np
import commands as c
import glob
import sys
import pickle as p
import os

Warning_Limit = 3
kB = 1.380648*6.02214129/1000.0
conv = 4.184
warnings = []

def getEnergy(fileName, Warning_Limit = 2., convert = 1.):
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

    energy = MBAR * kB * T / convert
    return energy[0],energy[1],warn

box = {}
directories = ['pme', 'rf']

for d in directories:
    box[d] = {}
    files = glob.glob("%s/*/results.pickle" % d)
    for f in files:
        num = f.split('/')[1].split('cyc')[-1]
        print num
        box[d][num] = {}
        
        # Get box size
        size = c.getoutput('tail -n 1 %s/cyc%s/prod.0.gro' % (d, num))
        size = float(size.strip().split(' ')[0].strip())
        box[d][num]['size'] = size

        En, Un, warn = getEnergy(f, convert = conv) 
        box[d][num]['energy'] = [En, Un]

print box
p.dump(box, open('boxSizeData.p','wb'))
