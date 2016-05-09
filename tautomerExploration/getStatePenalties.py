# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# This script reads results from ligprep calculations (Schrodinger tool) and saves the state penalty for the first tautomer in each file. 

import pickle
import numpy as np
import glob

# Location for ligprep file
maeFiles = glob.glob("MoleculeFiles/ligprep_SAMPL5_*.mae")
kBT = 0.001987207 * 298.15 # In kcal/mol 

# Load file with pKa Corrections already saved
d = pickle.load(open('dictionary_pKaCorrected.p','rb'))
# Create list for output file
output = ['SAMPL ID, logP, basic pKa, acidic pKa, largest pKa, state penalty\n']

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

    # Update dictionary
    d[samplID]['StatePenaltyCorrection'] = logPj
    logP = d[samplID]['LogD_calc']
    logD = logP[0] + logPj
    d[samplID]['logD_stateCorrected'] = [logD, logP[1]]
    # Start line for output file
    data = samplID
    for k in ['LogD_calc', 'LogD_baseCorrected','LogD_acidCorrected','LogD_oneCorrected','logD_stateCorrected']:
        data = data +', %.2f' % d[samplID][k][0]
    print data
    output.append(data+'\n')

fN = open('allLogDs.txt','w')
fN.writelines(output)
fN.close()
pickle.dump(d, open('dictionary_statePenalty.p','wb'))
