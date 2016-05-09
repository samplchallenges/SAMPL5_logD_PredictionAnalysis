# Caitlin C Bannan
# Mobley Group, University of California Irvine
# Prints error analysis data to text files and uses tools module to create histograms of that data.  

import pickle
from sigfig.sigfig import *
import sys
import glob
import numpy as np
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')

# Load Dictionaries with Data
regData = pickle.load(open('../DataFiles/predictions.p','rb'))
# ================================================================================
# Make histogram plots by error analysis
# ================================================================================
metrics = ['AveErr', 'RMS','AUE','tau','R', 'maxErr', 'percent', 'error slope', 'CorrectLipinski', 'compare slope']
pm = "+/-" 

# top line for data files
openLine = "Submission Number"
for m in metrics:
    if m == "percent":
        openLine += ", Percent Correct Sign"
    else:
        openLine = openLine + ", " + m

for (bat, batches) in [('batch0', 'batch0'),('batch1', 'batches0-1'),('batch2', 'batches0-1-2')]:
    keys = [k for k in regData.keys() if regData[k].has_key(bat)]
    subIDs = ["%02d" % k for k in keys]

    # Make all metric histogram plots:
    for metric in metrics:
        print "Making statistics histograms for ", metric
        # Save data to list if the id has this batch
        vals = [regData[k][bat][metric][0] for k in keys]
        dvals = [regData[k][bat][metric][1] for k in keys]
        # Use tool to sort data and plot it
        title = "Performance by Submission ID for %s" % batches
        print metric, min(vals), max(vals)
        fileName = "../statsPlots/%s_%s.pdf" % (metric, batches)

        # Make histograms of each error metric, with appropriate sorting. 
        if metric == 'error slope' or metric == 'compare slope':
            tools.histPlot(subIDs, vals, dvals, "Submission Number", metric, title, option = 'close to 1', fileName = fileName, absolute = False, widOption = 3)
        elif metric in ['R', 'tau']:
            tools.histPlot(subIDs, vals, dvals, "Submission Number", metric, title, option = 'reverse', fileName = fileName, absolute = False, widOption = 3)
        elif metric == 'CorrectLipinski':
            tools.histPlot(subIDs, vals, dvals, "Submission Number", "Correct Lipinski Rule", title, option = 'reverse', fileName = fileName, widOption = 3)
        elif metric == 'percent':
            tools.histPlot(subIDs, vals, dvals, "Submission Number", "correct sign (%%)", title, option = 'reverse', fileName = fileName, widOption = 3)
        else: # All other metrics
            tools.histPlot(subIDs, vals, dvals, "Submission Number", metric, title, fileName = fileName, widOption = 3  )
    
    # Make output file for this batch
    output = [openLine+'\n']

    for num, e in regData.items(): 
        if not e.has_key(bat):
            continue
        line = "%02d" % num
        for m in metrics:
            met = e[bat][m]
            try:
                line += ", %s %s %s" % (round_unc(met[0], met[1]), pm, round_sf(met[1], 1))
            except:
                line += ", %.0f %s %.0f" % (met[0], pm, met[1])
                print num, met, m
        output.append(line+'\n')

    # Save file
    fN = open("../DataFiles/ErrorMetricsBySubmission_%s.txt" % batches,'w')
    fN.writelines(output)
    fN.close()
