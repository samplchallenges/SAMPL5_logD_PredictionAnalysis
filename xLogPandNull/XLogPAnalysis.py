import pickle
from sigfig.sigfig import *
import sys
import glob
import numpy as np
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')
from openeye.oechem import *
from openeye.oemolprop import *
from openeye.oeiupac import *


#========================================================================
# Constants we'll need later:
bootits = 1000 # number bootstrap iterations
#========================================================================
# Load lists of molecule IDs by batch for dataAnalysis
batches = pickle.load(open('../DataFiles/batches.p','rb'))
# Load Experimental data and make lists by batch
Exp = pickle.load(open('../DataFiles/experimental.p','rb'))
# Load data by molecule for box and whisker plot
moleculeData = pickle.load(open('../DataFiles/moleculeData.p','rb'))

#========================================================================
# Giant fot loop that does a lot of things
# Now get statistics compared to experimental and add it to 
# for k,e in regData.items():
# Using only one prediction so I'm calling it e to match the old code:
e = {}
keys = sorted(Exp.keys())
for cid in keys:
    print cid
    smile = Exp[cid]['Smiles']
    # Generate OEMol
    mol = OEMol()
    OEParseSmiles(mol, smile)
    #Get logP
    xlogP = OEGetXLogP(mol)
    if not e.has_key('data'):
        e['data'] = {}
        e['data+'] = {}
    e['data'][cid] = [xlogP, 0.37]
    e['data+'][cid] = [xlogP - 1.45, 0.37] 

# Make Box and Whisker plots for each set of predictions
tools.BoxWhiskerByBatch(moleculeData, batches, e, predLabel = "XlogP Prediction", title = "XlogP Predictions Box and Whisker Plot", xAxis = "SAMPL5_IDnumber", fileName = "XLogP_boxPlot.pdf", Datakey = 'data')
tools.BoxWhiskerByBatch(moleculeData, batches, e, predLabel = "XlogP Prediction", title = "XlogP Predictions plus Linear Fit Box and Whisker Plot", xAxis = "SAMPL5_IDnumber", fileName = "XLogP_linear_boxPlot.pdf", Datakey = 'data+')

# Organize by batch
allExp = [ [Exp[k]['data'][0] for k in b] for b in batches ]
dallExp = [ [Exp[k]['data'][1] for k in b] for b in batches ]

calc = [ [e['data'][k][0] for k in b] for b in batches]
dcalc = [ [e['data'][k][1] for k in b] for b in batches]
calc2 = [ [e['data+'][k][0] for k in b] for b in batches]

# Use tools to plot data  
title = "Comparing predictions from Openeye's XLogP tool"
# Using larger of the two uncertainties for this plot
tools.ComparePlot(allExp, calc, title, "Experimental logD", "Predicted logD", dallExp, dcalc, ['batch%i'%0, 'batch%i'%1, 'batch%i'%2], "XLogP_compare.pdf")

# Use tools to plot data  
title = "Comparing predictions from Openeye's XLogP tool plus intercept correction"
# Using larger of the two uncertainties for this plot
tools.ComparePlot(allExp, calc2, title, "Experimental logD", "Predicted logD", dallExp, dcalc, ['batch%i'%0, 'batch%i'%1, 'batch%i'%2], "XLogP_linear_compare.pdf")

# Get Statistics for every batch that was provided using tools script
statCalc = calc[0] + calc[1] + calc[2]
statCalc2 = calc2[0] + calc2[1] + calc2[2]
dStatCalc = dcalc[0] + dcalc[1] + dcalc[2]
statExp = allExp[0] + allExp[1] + allExp[2]
dStatExp = dallExp[0] + dallExp[1] + dallExp[2] # This is a misnomer, it is the model uncertainty being used in this list later

e['AveErr'], e['RMS'], e['AUE'], e['tau'], e['R'], e['maxErr'], e['percent'], e['Rsquared'] = tools.stats_array(statCalc, statExp, dStatExp, bootits, "XLogP")
e['AveErr+'], e['RMS+'], e['AUE+'], e['tau+'], e['R+'], e['maxErr+'], e['percent+'], e['Rsquared'] = tools.stats_array(statCalc2, statExp, dStatExp, bootits, "XLogP")
# Get data for QQ plot
X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp, bootits)
# Store 'error slope'
e['error slope'] = [slope, dslope]
e['QQdata'] = [X,Y]
# Make and save QQ plot
title = "QQ Plot from Openeye's XLogP tool"
tools.makeQQplot(X, Y, slope, title, fileName = "XLogP_QQ.pdf")

X2, Y2, slope2, dslope2 = tools.getQQdata(statCalc2, statExp, dStatCalc, dStatExp, bootits)
# Store 'error slope'
e['error slope+'] = [slope2, dslope2]
e['QQdata+'] = [X2,Y2]
# Make and save QQ plot
title = "QQ Plot from Openeye's XLogP tool plus intercept correction"
tools.makeQQplot(X2, Y2, slope2, title, fileName = "XLogP_linear_QQ.pdf")




# Save as pickle files to be used in other files
pickle.dump(e, open('XLogP_predictions.p','wb'))
line0 = 'predictions'
line1 = 'XLogP'
line2 = 'XLogP + intercept'
for met in ['AveErr','RMS','AUE','tau','R','maxErr','percent','error slope']:
    m = e[met]
    line0 = line0 + ",\t %s" % met
    if m[1] == 0.0:
        line1 = line1 +",\t %.3f +/- %.3f" % (m[0], m[1])
    else:
        line1 = line1 + ",\t %s +/- %s" % (round_unc(m[0],m[1]), round_sf(m[1], 1))
    m = e[met+'+']
    if m[1] == 0.0:
        line2 = line2 +",\t %.3f +/- %.3f" % (m[0], m[1])
    else:
        line2 = line2 + ",\t %s +/- %s" % (round_unc(m[0],m[1]), round_sf(m[1], 1))

f = open('XlogPStats.txt','w')
f.writelines( [line0+'\n', line1+'\n', line2+'\n'])
f.close()
