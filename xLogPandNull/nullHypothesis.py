import pickle
from sigfig.sigfig import *
import numpy as np
import imp 
tools = imp.load_source('tools','../DataFiles/tools.py')

bootits = 1000 # number of bootstrap iterations

# Load experimental and batch data
batches = pickle.load(open('../DataFiles/batches.p','rb'))
experimental = pickle.load(open('../DataFiles/experimental.p','rb'))
moleculeData = pickle.load(open('../DataFiles/moleculeData.p','rb'))

# make dictionary for box/whisker plot
entry = {'data': {}}
for k, e in experimental.items():
    entry['data'][k] = [0.0, 0.0]
# create box and whisker plot
tools.BoxWhiskerByBatch(moleculeData, batches, entry, 'null hypothesis', 'SAMPL5_IDnumber', fileName = 'Null_boxPlot.pdf')

# Make lists of experimental data by batch
Exp = [ [experimental[k]['data'][0] for k in b] for b in batches ]
dExp = [ [experimental[k]['data'][1] for k in b] for b in batches ]

# combine into a single list
AllExp = Exp[0] + Exp[1] + Exp[2]
AlldExp = dExp[0] + dExp[1] + dExp[2]

# Null hypothesis assumes a 50:50 split between solvents so logD = 0
Calc = [ [0.0 for k in b] for b in batches]
# For the QQ plot and error slope, we will assume the error is 1 log unit
AllCalc = [1.0 for i in range(len(AllExp))]

# No calculated uncertainty for plotting purposes
dCalc  = [ [0.0 for k in b] for b in batches]
AlldCalc = [0.0 for i in range(len(AllExp))]

N = {} # dictionary for storing analysis

# Use tools to make a comparison plot of "prediction" verses experiment
tools.ComparePlot(Exp, Calc, "Null Hypothesis Comparison", "Experimental logD", "'Predicted' logD", dExp, dCalc, ['batch0','batch1','batch2'], "Null_Compare.pdf")

# Use tools module to perform error analysis
N['AveErr'], N['RMS'], N['AUE'], N['tau'], N['R'], N['maxErr'], N['percent'], N['Rsquared'] = tools.stats_array(AllCalc, AllExp, AlldExp, bootits)

# Do a QQ analysis, this is kind of silly with the assumed error, but I wanted to be consistent with analysis done on actual predictions
X, Y, slope, dslope = tools.getQQdata(AllCalc, AllExp, AlldCalc, AlldExp, bootits)
N['error slope'] = [slope, dslope]
N['QQdata'] = [X,Y]
tools.makeQQplot(X,Y, slope, "Null Hypothesis QQ Plot", fileName = "Null_QQ.pdf")

pickle.dump(N, open('NullData.p','wb'))

# Save data to text file
output = ['error metric,\t value,\t uncertainty\n']
for k, e in N.items():
    if k == 'QQdata':
        continue
    try:
        print k, '\t\t %s +/- %s' % (round_unc(e[0], e[1]), round_sf(e[1], 1))
    except:
        try:
            print k, '\t\t %.1f +/- %.1f' % (e[0], e[1])
        except:
            print k, '\t', e[0], '+/-', e[1]
    output.append('%s,\t %.3f,\t %.3f\n' % (k, e[0], e[1]))

f = open('../DataFiles/nullHypothesisData.txt','w')
f.writelines(output)
f.close()

