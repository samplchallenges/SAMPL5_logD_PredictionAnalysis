# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# Fall 2015
# Adapted from past scripts to extract results from tautomer runs. 

import numpy as np
import commands
import sys
import pickle as p
import os

Warning_Limit = 3
kB = 1.380648*6.02214129/1000.0
conv = 4.184
warnings = []

cyc = "./%s_cyc/results.pickle"
h2o = "./%s_h2o/results.pickle"
solvent_list = ['cyclohexane','water']

# get tautomer database
database = p.load(open('tautDictionary.p','rb'))

# get all results database so you can have results from the other one
oldData = p.load(open('initialDictionary.p','rb'))


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
    cycEn, cycUn, warn = getEnergy(cyc % num) 
    entry['taut1'] = oldData[num]
    entry['taut2'] = {}
    entry['taut2']['cyclohexane'] = [cycEn, cycUn]
    h2oEn, h2oUn, warn = getEnergy(h2o % num)
    entry['taut2']['water'] = [h2oEn, h2oUn]

    Dif = np.array([(cycEn - h2oEn), np.sqrt(h2oUn**2 + cycUn**2)])
    LogP = Dif/(np.log(10.)*kB*298.15)
    entry['taut2']['LogD_calc'] = LogP
    
p.dump(database, open('tautDictionary.p','wb'))

# =================================================================================
# Make LaTeX table with this data

output = ['\\begin{tabular}{| l | l l | l l |}\n', '\\hline\n']
output.append('& \\multicolumn{2}{|c|}{SAMPL5\\_050} & \\multicolumn{2}{|c|}{SAMPL5\\_083} \\\\\n')
output.append('& tautomer 1 &  tautomer 2 & tautomer 1 & tautomer 2 \\\\ \n')
output.append('\\hline')

title = ['$\\Delta G_{hydration}$', '$\\Delta G_{cyclohexane}$', '$\\log P_{cyc/wat}$']
for num in ['SAMPL5_050', 'SAMPL5_083']:
    print num
    for idx, key in enumerate(['cyclohexane', 'water', 'LogD_calc']):
        if idx == 0 or idx == 1:
            # convert to kCal /mol
            t1 = database[num]['taut1'][key]
            t2 = database[num]['taut2'][key]
            t1 = [t1[0] /conv, t1[1] / conv]
            t2 = [t2[0] / conv, t2[1] / conv]
        else:
            t1 = database[num]['taut1'][key]
            t2 = database[num]['taut2'][key]
        
        print key
        print 'taut1:', t1
        print 'taut2:', t2
        print

import glob

# Location for ligprep file
maeFiles = glob.glob("../../MoleculeFiles/ligprep_SAMPL5_083*.mae")
kBT = 0.001987207 * 298.15 # In kcal/mol 

# This is where in the ligprep file the data we want is stored. 
featureKey ="r_epik_State_Penalty" 

for f in maeFiles:
    # Read lines from file
    File = open(f, 'r')
    fileLines = File.readlines()
    File.close()

    # Get SAMPLId
    num = f.split('.')[0].split('_')[-1]
    samplID = "SAMPL5_"+num
    # File start of first variation (first occurance of "f_m_ct"
    lines = [l.strip().split(' ')[0] for l in fileLines]
    lines = lines[lines.index("f_m_ct"):]

    # Find location of the key for the feature you're looking for 
    key = lines.index(featureKey)
    # Find the divide between keys and entries
    divide = lines.index(":::")

    # Find Energy
    penaltyIdx = divide + key
    penalty = float(lines[penaltyIdx])

    # Convert to log based correction:
    logPj = -penalty / (kBT * np.log(10)) 

    print f
    print penalty
    print logPj
    print 
    
