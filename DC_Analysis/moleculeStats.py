# Written by Caitlin C Bannan
# Mobley Group, University of California Irvine
# March 2016
# Uses dictionary already created of data from the SAMPL5 challenge organized my molecule to make data tables which are saved to the DataFiles directory 

import pickle
from sigfig.sigfig import *
import sys
import glob
import numpy as np
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')

M = pickle.load(open('../DataFiles/moleculeData_topHalf.p','rb'))
# ================================================================================
# Make histogram plots by error analysis
# ================================================================================
metrics = ['AveErr', 'RMS','AUE','maxErr', 'percent', 'error slope']
pm = "+/-" 

# top line for data files
openLine = "Molecule ID, Average Predicted, Experimental"
for m in metrics:
    if m == "percent":
        openLine += ", Percent Correct Sign"
    else:
        openLine = openLine + ", " + m

keys = [k for k in M.keys()]
subIDs = [k.split('_')[1] for k in keys]

# Make all metric histogram plots:
for metric in metrics:
    print "Making statistics histograms for ", metric
    # Save data to list if the id has this batch
    vals = [M[k][metric][0] for k in keys]
    dvals = [M[k][metric][1] for k in keys]
    # Use tool to sort data and plot it
    print metric, min(vals), max(vals)
    fileName = "../statsPlots/%s_byMolecule_topHalf.pdf" % metric
    title = "Performance by molecule ID"
    # Determine how to sort
    if metric == 'error slope':
        tools.histPlot(subIDs, vals, dvals, "SAMPL5_IDnumber", metric, title, option = 'close to 1', fileName = fileName)
    elif metric == 'percent':
        tools.histPlot(subIDs, vals, dvals, "SAMPL5_IDnumber", "correct sign (%%)", title, option = 'reverse', fileName = fileName)
    else: # All other metrics
        tools.histPlot(subIDs, vals, dvals, "SAMPL5_IDnumber", metric, title, fileName = fileName)

output = [openLine+'\n']
for k in sorted(keys): 
    calc = np.average(np.array(M[k]['calc']))
    exp = M[k]['exp'][0]
    line = k + ", %.2f, %.2f" % (calc, exp)
    for m in metrics:
        met = M[k][m]
        try:
            line += ", %s %s %s" % (round_unc(met[0], met[1]), pm, round_sf(met[1], 1))
        except:
            line += ", %.0f %s %.0f" % (met[0], pm, met[1])
    output.append(line+'\n')

fN = open("../DataFiles/ErrorMetricByMolecule.txt", 'w')
fN.writelines(output)
fN.close()
