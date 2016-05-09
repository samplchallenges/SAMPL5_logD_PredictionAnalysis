# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
"""
Organizes data by molecule and saves to a new dictionary. Also creates QQ and comparison plots.
"""
import pickle 
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')
import numpy as np

bootits = 1000 # Number of bootstraps

# Load experimental and predicted data and ID numbers by batch
expData = pickle.load(open('../DataFiles/experimental.p','rb'))
batches = pickle.load(open('../DataFiles/batches.p','rb'))
calcData = pickle.load(open('../DataFiles/predictions.p','rb'))

# create dictionary to store data by molecule
molData = {}

for b, batch in enumerate(batches):
    bat = 'batch%i' % b
    print bat
    # Submission IDs that submitted this batch
    SIDs = [k for k in calcData.keys() if calcData[k].has_key(bat)]

    # for each molecule ID save experimental and predicted data and compute error analysis
    for k in batch:
        molData[k] = {}
        print '\t\t %.2f' % expData[k]['data'][0]
        # Store lists of experimental and calculated values for each molecule
        molData[k]['exp'] = [expData[k]['data'][0] for i in range(len(SIDs))]
        molData[k]['dexp'] = [expData[k]['data'][1] for i in range(len(SIDs))]
        molData[k]['dcalc_stat'] = [calcData[SID]['data'][k][1] for SID in SIDs]
        molData[k]['dcalc_mod'] = [calcData[SID]['data'][k][2] for SID in SIDs]
        molData[k]['calc'] = [calcData[SID]['data'][k][0] for SID in SIDs]
        
        # Error analysis for this molecule 
        molData[k]['AveErr'], molData[k]['RMS'],molData[k]['AUE'],molData[k]['tau'],molData[k]['R'],molData[k]['maxErr'],molData[k]['percent'], molData[k]['Rsquared'] = tools.stats_array(molData[k]['calc'], molData[k]['exp'], molData[k]['dexp'], bootits, sid = k)

        # QQ plot for this molecule
        X, Y, slope, dslope = tools.getQQdata(molData[k]['calc'], molData[k]['exp'], molData[k]['dcalc_mod'], molData[k]['dexp'], bootits) 
        molData[k]['error slope'] = [slope, dslope]
        molData[k]['QQdata'] = [X,Y]
        title = "QQ Plot for %s" % k
        tools.makeQQplot(X, Y, slope, title, fileName = "../QQPlots/%s_QQ.pdf" % k)

pickle.dump(molData, open('../DataFiles/moleculeData.p','wb'))
