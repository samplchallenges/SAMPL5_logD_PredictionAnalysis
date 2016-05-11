# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# reads text file provided by Frank Pickard (NIH) with his state penalties. 
# Addes logD calculated with these penalties to the dictionary
import pickle
import numpy as np
import glob

# Load Frank's penalty file
f = open('DataTables/penalties_fromPickard.txt', 'r')
lines = f.readlines()
f.close

# Redata from file
data = [l.split('   ') for l in lines]
data = [[l[0], float(l[1])] for l in data]

# Load dictionary with penalties calculated with Schrodiner's ligprep
d = pickle.load(open('dictionary_Corrected.p','rb'))

# Save Frank's data to the dictionary
for [num, pen] in data:
    SAMPL = 'SAMPL5_%s' % num
    d[SAMPL]['Pickard'] = pen
    d[SAMPL]['logPickard'] = pen / 1.36

# Make output list to make new text file
output = ['# Corrections such that logD = logP + correction\n', 'SAMPL5_5,\t Pickard,\t Epik\n']

# Make a row in the output file for each SAMPL5 molecule
for num in sorted(d.keys()):
    line = "%s,\t  %.3f,\t  %.3f\n" % (num, d[num]['logPickard'], d[num]['StatePenaltyCorrection'])
    output.append(line)

# Output comparison file. 
f = open('DataTables/ComparingPenalties.txt','w')
f.writelines(output)
f.close()

# Start output for all data table
output = ['SAMPL ID, logP, basic pKa, acidic pKa, largest pKa, Epik penalty, Pickard penalty, experiment\n']
exp = pickle.load(open('../DataFiles/experimental.p','rb'))

for samplID, e in d.items():
    # Convert to log based correction:
    logPj = d[samplID]['logPickard']

    # Update dictionary
    logP = d[samplID]['LogD_calc']
    logD = logP[0] + logPj
    d[samplID]['logD_PickardCorrected'] = [logD, logP[1]]
    data = samplID
    for k in ['LogD_calc', 'LogD_baseCorrected','LogD_acidCorrected','LogD_oneCorrected','logD_stateCorrected', 'logD_PickardCorrected']:
        data = data +', %.2f' % d[samplID][k][0]
    data = data + ', %.2f' % exp[samplID]['data'][0]
    print data
    output.append(data+'\n')

fN = open('DataTables/allLogDs.txt','w')
fN.writelines(output)
fN.close()
pickle.dump(d, open('dictionary_Corrected.p','wb'))
