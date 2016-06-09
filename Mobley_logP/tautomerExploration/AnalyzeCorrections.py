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
# number bootstrap iterations
bootits = 1000
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
database = pickle.load(open('dictionary_Corrected.p','rb'))
#========================================================================
# statistical uncertainty, I reported the same value for everything so we don't need to recreate it each time
dStatCalc = [1.4 for key in [batches[0] + batches[1] + batches[2] ] ] 

# Now get statistics compared to experimental and add it to 
output = ['Type of Calculation, AveErr, RMS, AUE, tau, R, maxErr, percent correct sign, error slope \n']

labels = ['original "logP"', 'Pickard corrections', 'Epik State Penalty', 'largest pKa correction', 'acidic pKa Correction', 'basic pKa Correction']

short = ['original','Pickard','Epik','pKa_largest','pKa_acidic','pKa_basic']

base = {}
for idx, logDkey in enumerate(['LogD_calc', 'logD_PickardCorrected', 'logD_stateCorrected', 'LogD_oneCorrected', 'LogD_acidCorrected','LogD_baseCorrected']):
    print labels[idx]

    # get predicted value for this data set
    calc = [ [database[key][logDkey][0] for key in batches[i] ] for i in range(3) ]
    statdcalc = [ [database[key][logDkey][1] for key in batches[i] ] for i in range(3) ]

    # Use tools to plot data  
    title = "Comparing predictions with %s correction added" % short[idx]
    tools.ComparePlot(allExp, calc, title, "Experimental logD", "Predicted logD", dallExp, statdcalc, ['batch%i'%0, 'batch%i'%1, 'batch%i'%2], "Plots/Compare_%s.pdf" %short[idx], limits = [-11, 7.5], wOption = 3)

    # Perform error analysis
    statCalc = calc[0] + calc[1] + calc[2]
    AveErr, RMS, AUE, tau, R, maxErr, percent, Rsquared = tools.stats_array(statCalc, statExp, dStatExp, bootits, short[idx])
    base[logDkey] = {}
    base[logDkey]['AveErr'] = AveErr
    base[logDkey]['RMS'] = RMS
    base[logDkey]['AUE'] = AUE
    base[logDkey]['tau'] = tau
    base[logDkey]['R'] = R
    base[logDkey]['maxErr'] = maxErr
    base[logDkey]['percent'] = percent  

    # Get data for QQ plot
    X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp, bootits)
    # Make and save QQ plot
    title = "QQ Plot for %s" % labels[idx]
    tools.makeQQplot(X, Y, slope, title, fileName = "Plots/QQ_%s.pdf" % short[idx])
    base[logDkey]['error slope'] = [slope, dslope]
      
    # Organize data to print into table
    line = labels[idx]
    for met in [AveErr, RMS, AUE, tau, R, maxErr, percent, [slope,dslope]]:
        if met[1] == 0.0:
            line = line + ",\t %.3f +/- %.3f" % (met[0], met[1])
        else:
            line = line + ",\t %s +/- %s" % (round_unc(met[0], met[1]), round_sf(met[1], 1))

    output.append(line+'\n')

# Add Klamt Data to comparison
klamt = pickle.load(open('../DataFiles/predictions.p','rb'))[16]
line = 'Klamt'
for met in ['AveErr','RMS','AUE','tau','R','maxErr','percent','error slope']:
    m = klamt['batch2'][met]
    if m[1] == 0.0:
        line = line +",\t %.3f +/- %.3f" % (m[0], m[1])
    else:
        line = line + ",\t %s +/- %s" % (round_unc(m[0],m[1]), round_sf(m[1], 1))

output.append(line+'\n')


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
tools.ComparePlot(expAll, predAll, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logP', 'logD by pKa'], "Plots/Compare_changing_largepKa.pdf", limits = [-11.5, 7.5], symbols = ['bs','ro','mo','co'], wOption = 3)
 
title = "Comparing predictions for largest pKa correction to epik state penalty corrections"
Epikpred = np.array([logD, logDEpik])
tools.ComparePlot(expAll, Epikpred, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logD by pKa', 'logD by state penalty'], "Plots/Compare_changing_state.pdf", limits = [-11.5, 7.5], symbols = ['ro','gD'], wOption = 3)

#def ComparePlot(x, y, Title, XLabel, YLabel, xerr, yerr, labels, fileName = None, limits = None, symbols = None):
title = "Comparing predictions for 'logP' correct by pKa and state penalty"
tools.ComparePlot(np.array([exp, exp, exp]), np.array([logP, logD, logDEpik]), title, "Experimental logD", "Predicted logD", np.array([dexp, dexp, dexp]), np.array([dlog, dlog, dlog]), ['logP', 'logD by pKa', 'logD by state penalty'], "Plots/Compare_changing_all.pdf", limits = [-11.5, 7.5], symbols = ['bs','ro','gD'], wOption = 3)


# ======================================================================
# The following bit includes analysis performed when we only had pKa corrections

keys = database.keys()
titles = ['Larger pKa Corrected logD', 'basic pKa Corrected logD', 'acidic pKa Corrected logD']
files = ['largestpKa','basicpKa','acidicpKa']
exp = np.array([Exp[k]['data'][0] for k in keys])
dexp = np.array([Exp[k]['data'][1] for k in keys])
logP = np.array([database[k]['LogD_calc'][0] for k in keys])
dlog = np.array([database[k]['LogD_calc'][1] for k in keys]) 

for i, label in enumerate(['LogD_oneCorrected','LogD_baseCorrected','LogD_acidCorrected']):
    logD = np.array([database[k][label][0] for k in keys])
    idx = [a for a in range(len(logD)) if abs(logP[a] - logD[a]) > 0.001]
    logP_changing = logP[idx]
    logD_changing = logD[idx]
    dlog_changing = dlog[idx]
    exp_changing = exp[idx]
    dexp_changing = dexp[idx]

    # Add error analysis for logP (only changing values)
    AveErr, RMS, AUE, tau, R, maxErr, percent, Rsquared = tools.stats_array(logP_changing, exp_changing, dexp_changing, bootits, "logP changing")
    # Get data for QQ plot
    X, Y, slope, dslope = tools.getQQdata(logP_changing, exp_changing, dlog_changing, dexp_changing, bootits)
    line = 'limited logP %s' % files[i]
    for met in [AveErr, RMS, AUE, tau, R, maxErr, percent, [slope,dslope]]:
        line = line + "\t, %s +/- %s" % (round_unc(met[0], met[1]), round_sf(met[1], 1))
    output.append(line+'\n')

    # Add error analysis for logD (only changing values)
    AveErr, RMS, AUE, tau, R, maxErr, percent, Rsquared = tools.stats_array(logD_changing, exp_changing, dexp_changing, bootits, "logD changing")
    # Get data for QQ plot
    X, Y, slope, dslope = tools.getQQdata(logD_changing, exp_changing, dlog_changing, dexp_changing, bootits)
    line = 'limited logD %s' % files[i]
    for met in [AveErr, RMS, AUE, tau, R, maxErr, percent, [slope,dslope]]:
        line = line + "\t, %s +/- %s" % (round_unc(met[0], met[1]), round_sf(met[1], 1))
    output.append(line+'\n')

    # Make Comparison Plots
    predAll = np.array([logP, logD])
    dpredAll = np.array([dlog, dlog])
    expAll = np.array([exp, exp])
    dexpAll = np.array([dexp, dexp])
    title = "Comparing predictions for 'logP' and %s" % titles[i]
    # Using larger of the two uncertainties for this plot
    tools.ComparePlot(expAll, predAll, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logP', 'logD'], "Plots/Compare_%s_logP.pdf" % files[i], limits =[-11.5, 7.5],  symbols = ['bs','ro','mo','co'], wOption = 3)
     
    predAll = np.array([logP_changing, logD_changing])
    dpredAll = np.array([dlog_changing, dlog_changing])
    expAll = np.array([exp_changing, exp_changing])
    dexpAll = np.array([dexp_changing, dexp_changing])
    title = "Comparing predictions for only changing 'logP' and %s" % titles[i]
    # Using larger of the two uncertainties for this plot
    tools.ComparePlot(expAll, predAll, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logP', 'logD'], "Plots/Compare_%s_limited.pdf" % files[i], limits = [-11.5, 7.5], symbols = ['bs','ro','mo','co'], wOption = 3)
     
f = open('DataTables/ErrorAnalysis_LogDCorrections.txt','w')
f.writelines(output)
f.close()

pickle.dump(base, open('CorrectionStats.p', 'wb'))
