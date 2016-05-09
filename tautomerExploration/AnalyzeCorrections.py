# Written by Caitlin C Bannan
# Mobley Group, University of California, Irvine
# March 2016
# This script was added to with each new tautomer enumeration or state penalty calculation that we were provided with. 

import pickle
import sys
from sigfig.sigfig import *
import glob
import numpy as np
import imp 
tools = imp.load_source('tools','../DataFiles/tools.py')

#========================================================================
# Constants we'll need later:
bootits = 1000 # number bootstrap iterations
#========================================================================
# Load lists of molecule IDs by batch for dataAnalysis
batches = pickle.load(open('../DataFiles/batches.p','rb'))
# Load Experimental data and make lists by batch
Exp = pickle.load(open('../DataFiles/experimental.p','rb'))

allExp = [ [Exp[k]['data'][0] for k in b] for b in batches ]
dallExp = [ [Exp[k]['data'][1] for k in b] for b in batches ]
statExp = allExp[0] + allExp[1] + allExp[2]
dStatExp = dallExp[0] + dallExp[1] + dallExp[2]

# Load Prediction Dictionary
database = pickle.load(open('dictionary_statePenalty.p','rb'))
#========================================================================
# Now get statistics compared to experimental and add it to 
dStatCalc = [1.4 for key in [batches[0] + batches[1] + batches[2] ] ] 

output = ['Type of Calculation, AveErr, RMS, AUE, tau, R, maxErr, percent correct sign, error slope \n']

labels = ['original "logP"', 'Pickard corrections', 'Epik State Penalty', 'largest pKa correction', 'acidic pKa Correction', 'basic pKa Correction']

short = ['original','Pickard','Epik','pKa_largest','pKa_acidic','pKa_basic']

for idx, logDkey in enumerate(['LogD_calc', 'logD_PickardCorrected', 'logD_stateCorrected', 'LogD_oneCorrected', 'LogD_acidCorrected','LogD_baseCorrected']):
    continue
    print labels[idx]
    calc = [ [database[key][logDkey][0] for key in batches[i] ] for i in range(3) ]
    statdcalc = [ [database[key][logDkey][1] for key in batches[i] ] for i in range(3) ]
    # Use tools to plot data  
    title = "Comparing predictions with %s correction added" % short[idx]
    # Using larger of the two uncertainties for this plot
    tools.ComparePlot(allExp, calc, title, "Experimental logD", "Predicted logD", dallExp, statdcalc, ['batch%i'%0, 'batch%i'%1, 'batch%i'%2], "Plots/Compare_%s.pdf" %short[idx], [-11, 7.5])
    # Get Statistics for every batch that was provided using tools script
    statCalc = calc[0] + calc[1] + calc[2]
    AveErr, RMS, AUE, tau, R, maxErr, percent = tools.stats_array(statCalc, statExp, dStatExp, bootits, short[idx])
    # Get data for QQ plot
    X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp, bootits)
    # Make and save QQ plot
    title = "QQ Plot for %s" % labels[idx]
    tools.makeQQplot(X, Y, slope, title, fileName = "Plots/QQ_%s.pdf" % short[idx])

    line = labels[idx]
    for met in [AveErr, RMS, AUE, tau, R, maxErr, percent, [slope,dslope]]:
        if met[1] == 0.0:
            line = line + ",\t %.3f +/- %.3f" % (met[0], met[1])
        else:
            line = line + ",\t %s +/- %s" % (round_unc(met[0], met[1]), round_sf(met[1], 1))

    output.append(line+'\n')

# Add Klamt Data to comparison
klamt = pickle.load(open('../predictions_byNum.p','rb'))[16]
line = 'Klamt'
for met in ['AveErr','RMS','AUE','tau','R','maxErr','percent','error slope']:
    m = klamt['batch2'][met]
    if m[1] == 0.0:
        line = line +",\t %.3f +/- %.3f" % (m[0], m[1])
    else:
        line = line + ",\t %s +/- %s" % (round_unc(m[0],m[1]), round_sf(m[1], 1))

output.append(line+'\n')
f = open('ErrorAnalysis_LogDCorrections.txt','w')
f.writelines(output)
f.close()


#######################################################################################################
# Making Plots David Requested
keys = database.keys()
files = ['largestpKa','basicpKa','acidicpKa']
exp = np.array([Exp[k]['data'][0] for k in keys])
dexp = np.array([Exp[k]['data'][1] for k in keys])
logP = np.array([database[k]['LogD_calc'][0] for k in keys])
dlog = np.array([database[k]['LogD_calc'][1] for k in keys]) 

logD = np.array([database[k]['LogD_oneCorrected'][0] for k in keys])
logDEpik = np.array([database[k]['logD_stateCorrected'][0] for k in keys])
print max(max(logD), max(logDEpik))
print min(min(logD), min(logDEpik))

# Make Comparison Plots
predAll = np.array([logP, logD])
dpredAll = np.array([dlog, dlog])
expAll = np.array([exp, exp])
dexpAll = np.array([dexp, dexp])
title = "Comparing predictions for 'logP' corrected by largest pKa"
# Using larger of the two uncertainties for this plot
tools.ComparePlot(expAll, predAll, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logP', 'logD by pKa'], "Plots/Compare_changing_largepKa.pdf", [-11.5, 7.5], ['bs','ro','mo','co'])
 
title = "Comparing predictions for largest pKa correction to epik state penalty corrections"
Epikpred = np.array([logD, logDEpik])
tools.ComparePlot(expAll, Epikpred, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logD by pKa', 'logD by state penalty'], "Plots/Compare_changing_state.pdf", [-11.5, 7.5], ['ro','gD'])

#def ComparePlot(x, y, Title, XLabel, YLabel, xerr, yerr, labels, fileName = None, limits = None, symbols = None):
title = "Comparing predictions for 'logP' correct by pKa and state penalty"
tools.ComparePlot(np.array([exp, exp, exp]), np.array([logP, logD, logDEpik]), title, "Experimental logD", "Predicted logD", np.array([dexp, dexp, dexp]), np.array([dlog, dlog, dlog]), ['logP', 'logD by pKa', 'logD by state penalty'], "Plots/Compare_changing_all.pdf", [-11.5, 7.5], ['bs','ro','gD'])


f = open('ErrorAnalysis_LogDCorrections.txt','w')
f.writelines(output)
f.close()

