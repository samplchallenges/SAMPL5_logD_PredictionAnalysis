# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# reads text file provided by Frank Pickard (NIH) with his state penalties. 

import pickle

# Load Frank's penalty file
f = open('Z_DGCORR_SOLV_ABSPKA', 'r')
lines = f.readlines()
f.close

# Redata from file
data = [l.split('   ') for l in lines]
data = [[l[0], float(l[1])] for l in data]

# Load dictionary with penalties calculated with Schrodiner's ligprep
a = pickle.load(open('penaltyDictionary.p','rb'))

# Save Frank's data to the dictionary
for [num, pen] in data:
    a[num]['Pickard'] = pen
    a[num]['logPickard'] = pen / 1.36

# Make output list to make new text file
output = ['# Corrections such that logD = logP + correction\n', 'SAMPL5_5,\t Pickard,\t Epik\n']

# Make a row in the output file for each SAMPL5 molecule
for num in sorted(a.keys()):
    line = "%s,\t  %.3f,\t  %.3f\n" % (num, a[num]['logPickard'], a[num]['logPen'])
    output.append(line)

# Output comparison file. 
f = open('ComparingPenalties.txt','w')
f.writelines(output)
f.close()

pickle.dump(a, open('penaltyDictionary.p','wb'))
