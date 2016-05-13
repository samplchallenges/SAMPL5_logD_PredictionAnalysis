# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# This script makes the same comparison plots where logD predictions are plotted against experimental values, but this time the molecules are colorcoded by number of tautomers that molecule could have, based on openeye's quacpac tool

import numpy as np
import imp 
tools = imp.load_source('tools','../DataFiles/tools.py')
import pickle

# Load experimental data and prediction data dictionaries
expDict = pickle.load(open('../DataFiles/experimental.p','rb'))
predDict = pickle.load(open('../DataFiles/predictions.p','rb'))

# Group Labels
groupLabels = ['1 tautomer', '2-4 tautomers', '6-9 tautomers', '10-19 tautomers', '>19 tautomers']
# We will make a separate plot for each set of predictions
for num, e in predDict.items():
    print num
    # Make lists for predictions, experiment, and uncertainties
    # These will be in the order number of tautomers [=1, 2-4, 6-9, 10-19, >=20]
    calc = [ [], [], [], [], [] ]
    dcalc = [ [], [], [], [], [] ]
    exp = [ [], [], [], [], [] ]
    dexp = [ [], [], [], [], [] ]
    tautKeys = [ [], [], [], [], [] ]
    # Add data by SAMPL_ID
    for sid, d in e['data'].items():
        # number of tautomers
        t = expDict[sid]['tautomers']
        # Find index based on number of tautomers
        if t == 1:
            idx = 0
        elif t < 5:
            idx = 1
        elif t < 10:
            idx = 2
        elif t < 20:
            idx = 3
        else:
            idx = 4

        # Save data to list
        calc[idx].append(d[0])
        dcalc[idx].append(d[1])
        exp[idx].append(expDict[sid]['data'][0])
        dexp[idx].append(expDict[sid]['data'][1])
        tautKeys[idx].append(sid)
    # Plot information
    exp = np.array(exp)
    calc = np.array(calc)
    dexp = np.array(dexp)
    dcalc = np.array(dcalc)

    title = "Tautomer Comparison Plot %02d" % num
    fileName = "../ComparePlots/%02d_tautomers.pdf" % num
    tools.ComparePlot(exp, calc, title, "Experimental logD", "Predicted logD", dexp, dcalc, groupLabels, fileName, wOption = 2) 

# Make datatable for molecules in each tautomer set
output = ['# tautomer batches\n']
for i, Set in enumerate(tautKeys):
    output.append("%s\n" % groupLabels[i])
    output.append("%s\n" % ', '.join(Set))

f = open("../DataFiles/tautomerBatches.txt", "w")
f.writelines(output)
f.close()

# Now lets look at data by molecule as well
molDict = pickle.load(open('../DataFiles/moleculeData.p','rb'))

for i, Set in enumerate(tautKeys):
    AUEs = [molDict[k]['AveErr'][0] for k in Set]
    print groupLabels[i]
    print "%.2f, %.2f, %.2f" % (np.min(AUEs), np.max(AUEs), np.average(AUEs))

