import pickle
from sigfig.sigfig import *
import glob
import numpy as np
import tools

def getBatch(dataSet, batches):
    """
    Takes a dataSet with keys that should be in one list in batches. 
    Returns an integer for the last batch the dataset has
    """

    for (i, b) in enumerate(batches):
        missing = len(b) - len(set(b).intersection(dataSet.keys()))
        if missing > 0:
            return i -1
    return i

#========================================================================
# Constants we'll need later:
bootits = 1000 # number bootstrap iterations
#========================================================================
# Load lists of molecule IDs by batch for dataAnalysis
batches = pickle.load(open('../batches.p','rb'))
# Load Experimental data and make lists by batch
Exp = pickle.load(open('experimental.p','rb'))
allExp = [ [Exp[k]['data'][0] for k in b] for b in batches ]
dallExp = [ [Exp[k]['data'][1] for k in b] for b in batches ]
statExp = allExp[0] + allExp[1] + allExp[2]
dStatExp = dallExp[0] + dallExp[1] + dallExp[2]

# Load Prediction Dictionary
database = pickle.load(open('dictionary_pKaCorrected.p','rb'))
#========================================================================
# Giant fot loop that does a lot of things
# Now get statistics compared to experimental and add it to 
dStatCalc = [1.4 for key in [batches[0] + batches[1] + batches[2] ] ] 
output = ['Type of Calculation, AveErr, RMS, AUE, tau, R, maxErr, percent correct sign, error slope \n']
labels = ['original "logP"', 'largest pKa correction', 'acidic pKa Correction', 'basic pKa Correction']
for logDkey in ['LogD_calc', 'LogD_oneCorrected', 'LogD_acidCorrected','LogD_baseCorrected']:
    calc = [ [database[key][logDkey][0] for key in batches[i] ] for i in range(3) ]
    statdcalc = [ [database[key][logDkey][1] for key in batches[i] ] for i in range(3) ]
    # Use tools to plot data  
    title = "Comparing predictions for %s" % logDkey
    # Using larger of the two uncertainties for this plot
    # tools.ComparePlot(allExp, calc, title, "Experimental logD", "Predicted logD", dallExp, statdcalc, ['batch%i'%0, 'batch%i'%1, 'batch%i'%2], "Compare_%s.pdf" % logDkey)
    # Get Statistics for every batch that was provided using tools script
    statCalc = calc[0] + calc[1] + calc[2]
    AveErr, RMS, AUE, tau, R, maxErr, percent = tools.stats_array(statCalc, statExp, dStatExp, bootits)
    # Get data for QQ plot
    X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp, bootits)
    # Make and save QQ plot
    title = "QQ Plot for %s" % logDkey
    tools.makeQQplot(X, Y, slope, title, fileName = "QQ_%s.pdf" % logDkey)

    line = logDkey
    for met in [AveErr, RMS, AUE, tau, R, maxErr, percent, [slope,dslope]]:
        line = line + "\t, %s +/- %s" % (round_unc(met[0], met[1]), round_sf(met[1], 1))
    output.append(line+'\n')

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
    AveErr, RMS, AUE, tau, R, maxErr, percent = tools.stats_array(logP_changing, exp_changing, dexp_changing, bootits)
    # Get data for QQ plot
    X, Y, slope, dslope = tools.getQQdata(logP_changing, exp_changing, dlog_changing, dexp_changing, bootits)
    line = 'limited logP %s' % files[i]
    for met in [AveErr, RMS, AUE, tau, R, maxErr, percent, [slope,dslope]]:
        line = line + "\t, %s +/- %s" % (round_unc(met[0], met[1]), round_sf(met[1], 1))
    output.append(line+'\n')

    # Add error analysis for logD (only changing values)
    AveErr, RMS, AUE, tau, R, maxErr, percent = tools.stats_array(logD_changing, exp_changing, dexp_changing, bootits)
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
    tools.ComparePlot(expAll, predAll, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logP', 'logD'], "Compare_%s.pdf" % files[i], ['bs','ro','mo','co'])
     
    predAll = np.array([logP_changing, logD_changing])
    dpredAll = np.array([dlog_changing, dlog_changing])
    expAll = np.array([exp_changing, exp_changing])
    dexpAll = np.array([dexp_changing, dexp_changing])
    title = "Comparing predictions for only changing 'logP' and %s" % titles[i]
    # Using larger of the two uncertainties for this plot
    tools.ComparePlot(expAll, predAll, title, "Experimental logD", "Predicted logD", dexpAll, dpredAll, ['logP', 'logD'], "Compare_%s_limited.pdf" % files[i], ['bs','ro','mo','co'])
     
f = open('pKaCorrectedErrorAnalysis.txt','w')
f.writelines(output)
f.close()

