# Written by Caitlin C Bannan
# Mobley Group, University of California, Irvine
# February 2016
# Used to analyze distribution coefficient predictions for SAMPL5 challenge

import pickle
import sys # Used to exit while testing code
import numpy as np
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')

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
# low and high limit for lipinski rule range
LipLowLim = -0.4 
LipHighLim = 5.6
#========================================================================

# Load lists of molecule IDs by batch for dataAnalysis
batches = pickle.load(open('../DataFiles/batches.p','rb'))

# Load Experimental data and make lists by batch
Exp = pickle.load(open('../DataFiles/experimental.p','rb'))
allExp = [ [Exp[k]['data'][0] for k in b] for b in batches ]
dallExp = [ [Exp[k]['data'][1] for k in b] for b in batches ]

# Load Prediction Dictionary
regData = pickle.load(open('../DataFiles/predictions.p','rb'))
moleculeData = pickle.load(open('../DataFiles/moleculeData.p','rb'))

# Make blank Box and Whisker Plot
tools.BoxWhiskerByBatch(moleculeData, batches, {}, title = "Box and Whisker Plot all Predictions", xAxis = "SAMPL5_IDnumber", fileName = "../boxPlots/boxplot_blank.pdf")
#========================================================================
# Giant fot loop that does a lot of things
# Now get statistics compared to experimental and add it to 
for num, e in regData.items():
    b = getBatch(e['data'],batches)
    if b < 2:
        print num, b
    continue

    # Make Box and Whisker plot
    title = "Box and Whisker Plot for Prediction Set %02d" % num
    tools.BoxWhiskerByBatch(moleculeData, batches, e, "%02d predictions" % num, title, 'SAMPL5_IDnumber', fileName = "../boxPlots/boxplot_%02d.pdf" % num)

    print "Analyzing Entry ", num, "..."
    calc = [ [e['data'][key][0] for key in batches[i] ] for i in range(b+1) ]
    # statistical error
    statdcalc = [ [e['data'][key][1] for key in batches[i] ] for i in range(b+1) ]
    # model uncertainty
    moddcalc = [ [e['data'][key][2] for key in batches[i] ] for i in range(b+1) ]
    
    # Use tools to plot data  
    title = "Comparing predictions for Submission %02d" % num
    title = "Submission %02d" % num

    # Using larger of the two uncertainties for this plot
    tools.ComparePlot(allExp[:b+1], calc, title, "Experimental logD", "Predicted logD", dallExp[:b+1], statdcalc, ['batch%i'%0, 'batch%i'%1, 'batch%i'%2], "../ComparePlots/%02d_compare.pdf" %num)
    # Perform Error Analysis for every batch that was provided using tools script
    statCalc = [] # calc list for statistics
    dStatCalc = [] # uncertainty in calc values for statistics
    statExp = [] # experimental value for statistics
    dStatExp = [] # uncertainty in experimental values 

    for i in range(b+1):
        print "Batch ", i

        # Added data for each new batch
        statCalc += calc[i]
        dStatCalc += moddcalc[i] 
        statExp += allExp[i]
        dStatExp += dallExp[i]
        bat = "batch%i" % i

        # Store data for each new batch in new sub dictionary
        e[bat] = {}

        # perform and store results of error analysis
        e[bat]['AveErr'], e[bat]['RMS'], e[bat]['AUE'], e[bat]['tau'], e[bat]['R'], e[bat]['maxErr'], e[bat]['percent'], e[bat]['Rsquared'] = tools.stats_array(statCalc, statExp, dStatExp, bootits, num)

        # Perform Lipinski Test and save information
        correct, falsePos, falseNeg = tools.getLipinskiData(statCalc, statExp, dStatExp, LipLowLim, LipHighLim, bootits)
        e[bat]['CorrectLipinski'] = np.array(correct) / float(len(statCalc))
        e[bat]['FalsePosLipinski'] = np.array(falsePos) / float(len(statCalc))
        e[bat]['FalseNegLipinski'] = np.array(falseNeg) / float(len(statCalc))

        # Calculate a slope for the experiment vs prediction plot
        e[bat]['compare slope'] = tools.getSlope(statCalc, statExp, dStatExp, bootits)

        # Get Data for QQ plot with tools module
        X, Y, slope, dslope = tools.getQQdata(statCalc, statExp, dStatCalc, dStatExp, bootits)
        # Store 'error slope'
        e[bat]['error slope'] = [slope, dslope]
        # Store QQ plot data
        e[bat]['QQdata'] = [X,Y]
        # Make and save 1 QQ plot for each prediction set
        if i == b: 
            title = "QQ Plot for %i for batches 0-%i" % (num, i) 
            tools.makeQQplot(X, Y, slope, title, fileName = "../QQPlots/%02d_QQ.pdf" % num)


sys.exit(1)
# Save as pickle files to be used in other files
pickle.dump(regData, open('../DataFiles/predictions.p','wb'))


