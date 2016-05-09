import pickle
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
batches = pickle.load(open('batches.p','rb'))
# Load Experimental data and make lists by batch
Exp = pickle.load(open('experimental_un.p','rb'))
Exp_low = pickle.load(open('experimental_low.p','rb'))
Exp_high = pickle.load(open('experimental_high.p','rb'))

allExp = [ [Exp[k]['data'][0] for k in bat] for bat in batches ]
dallExp_un = [ [Exp[k]['data'][1] for k in b] for b in batches ]
dallExp_low = [ [Exp_low[k]['data'][1] for k in b] for b in batches ]
dallExp_high = [ [Exp_high[k]['data'][1] for k in b] for b in batches ]

# Load Prediction Dictionary
regData = pickle.load(open('predictions.p','rb'))
testStats = {}
#========================================================================
# Giant fot loop that does a lot of things
# Now get statistics compared to experimental and add it to 
keys = ['1b3d','a4dd','602e','c410','232e']
for k in keys:
    e = regData[k]
    testStats[k+'_un'] = {}
    testStats[k+'_low'] = {}
    testStats[k+'_high'] = {}
    print "Analyzing Entry ", k, "..."
    b = getBatch(e['data'],batches)
    calc = [ [e['data'][key][0] for key in batches[i] ] for i in range(b+1) ]
    # statistical error
    statdcalc = [ [e['data'][key][1] for key in batches[i] ] for i in range(b+1) ]
    # model uncertainty
    moddcalc = [ [e['data'][key][2] for key in batches[i] ] for i in range(b+1) ]
    
    # Use tools to plot data  
    title = k # {will need to clarify this}

    # Get Statistics for every batch that was provided using tools script
    statCalc = []
    dStatCalc = []
    statExp = []
    dStatExp_un = []
    dStatExp_low = []
    dStatExp_high = []
    for i in range(b+1):
        print "Batch ", i
        # Added data for each new batch
        statCalc += calc[i]
        dStatCalc += moddcalc[i] 
        statExp += allExp[i]
        dStatExp_un += dallExp_un[i]
        dStatExp_low += dallExp_low[i]
        dStatExp_high += dallExp_high[i]
        bat = "batch%i" % i
        # Store data for each new batch
        if i != 2:
            continue

        testStats[k+'_un']['AveErr'], testStats[k+'_un']['RMS'],testStats[k+'_un']['AUE'], testStats[k+'_un']['tau'], testStats[k+'_un']['R'], testStats[k+'_un']['maxErr'], testStats[k+'_un']['percent'] = tools.stats_array(statCalc, statExp, dStatExp_un, bootits)
        testStats[k+'_low']['AveErr'], testStats[k+'_low']['RMS'],testStats[k+'_low']['AUE'], testStats[k+'_low']['tau'], testStats[k+'_low']['R'], testStats[k+'_low']['maxErr'], testStats[k+'_low']['percent'] = tools.stats_array(statCalc, statExp, dStatExp_low, bootits)
        testStats[k+'_high']['AveErr'], testStats[k+'_high']['RMS'],testStats[k+'_high']['AUE'], testStats[k+'_high']['tau'], testStats[k+'_high']['R'], testStats[k+'_high']['maxErr'], testStats[k+'_high']['percent'] = tools.stats_array(statCalc, statExp, dStatExp_high, bootits)
        # Get data for QQ plot
        X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp_un, bootits)
        # Store 'error slope'
        testStats[k+'_un']['error slope'] = [slope, dslope]
        X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp_low, bootits)
        testStats[k+'_low']['error slope'] = [slope, dslope]
        X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp_high, bootits)
        testStats[k+'_high']['error slope'] = [slope, dslope]


metrics = ['AveErr','RMS','AUE','tau','R','maxErr','percent','error slope']
pickle.dump(testStats, open('testStats.p','wb'))


