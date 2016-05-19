# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# May 2016
# Makes Table 2 for 

import pickle
import matplotlib.pyplot as plt
from pylab import *

# Molecule data
molData = pickle.load(open('../DataFiles/moleculeData.p','rb'))

# Get batches
batches = pickle.load(open('../DataFiles/batches.p','rb'))

# File formatting
output = ["\\begin{tabular}{| l | l | p{10cm}| }\n", "\\hline\n", "Compound & AUE & SMILES \\\\\n", "\\hline\n"]
csv = ["Compound, AUE, SMILES\n"]

for b, batch in enumerate(batches):
    for k in sorted(batch):
        # get mean unsigned error
        AUE = "$ %.1f \\pm %.1f $" % (molData[k]['AUE'][0], molData[k]['AUE'][1])

        # get SMILES string and adjust for special characters in latex
        smile = molData[k]['Smiles']
        #smile = smile.replace('\#', '\\\#')
        # smile = smile.replace('@', '{@}')
        # smile = smile.replace('\\', '\\\\')
        #smile = smile.replace('[', '\\[')
        #smile = smile.replace(']', '\\]')

        # Add data to output
        output.append("%s & %s & $%s$ \\\\ \n" % (k.replace('_', '\\_'), AUE, smile ))
        csv.append("%s, %s, %s\n" % (k, AUE, smile))
    output.append("\\hline \n")

output.append('\\hline \n')
output.append("\\end{tabular}\n")

f = open("MoleculeTable.tex", 'w')
f.writelines(output)
f.close()

f = open("MoleculeTable.csv", 'w')
f.writelines(csv)
f.close()

# keys = [k for k in sorted(molData)]
# MWs = [molData[k]['MW'] for k in keys]
# AUE = [molData[k]['AUE'][0] for k in keys]
# dAUE = [molData[k]['AUE'][1] for k in keys]

# fig = plt.figure(1)
# plt.xlabel('MW')
# plt.ylabel('AUE')
# ax = fig.add_subplot(111)
# ax.errorbar(MWs, AUE, yerr = dAUE, fmt = 'ko')
# savefig('testingMW.pdf')
