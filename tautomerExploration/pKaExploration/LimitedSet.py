import pickle
from sigfig.sigfig import *
import glob
import numpy as np
import tools
#========================================================================
# Constants we'll need later:
bootits = 1000 # number bootstrap iterations
diff = 0.01
#========================================================================
# Load Experimental data and make lists by batch
Exp = pickle.load(open('experimental.p','rb'))
# Load Prediction Dictionary
database = pickle.load(open('dictionary_pKaCorrected.p','rb'))
Klamt = pickle.load(open('../predictions_byNum.p','rb'))[16]['data']

limit_keys = []
for k, e in database.items():
    logD = e['LogD_oneCorrected'][0]
    logP = e['LogD_calc'][0]
    if abs(logD - logP) > diff:
        print k
        limit_keys.append(k)
print "There are ", len(limit_keys), "changed logDs"
limit_keys = sorted(limit_keys)
all_keys = sorted(database.keys())

allLogP = np.array([database[k]['LogD_calc'] for k in all_keys])
limitLogP = np.array([database[k]['LogD_calc']  for k in limit_keys])

allLogD = np.array([database[k]['LogD_oneCorrected']  for k in all_keys])
limitLogD = np.array([database[k]['LogD_oneCorrected']  for k in limit_keys])

allKlamt = np.array([Klamt[k] for k in all_keys])
limitKlamt = np.array([Klamt[k] for k in limit_keys])

allExp = np.array([Exp[k]['data'] for k in all_keys])
limitExp = np.array([Exp[k]['data'] for k in limit_keys])

output = ["# Compare the largest change from pKa corrected data to entry 16 results\n", "# Limited refers to only logP values changed by at least %.4f\n" % diff, 'data set,\t AveErr,\t RME,\t AUE,\t tau,\t R,\t maxErr,\t percent,\t error slope \n']
dataSet = ["All LogP", "All Corrected LogD", "All Klamt prediction", "Limited LogP", "Limited LogD", "Limited Klamt predictions"] 
for i, data in enumerate([allLogP, allLogD, allKlamt, limitLogP, limitLogD, limitKlamt]):
    print i
    print dataSet[i]
    if dataSet[i].split(' ')[0] == 'All':
        print "\t all data"
        exp = allExp
    else:
        exp = limitExp
        print '\t limited data'
    if dataSet[i].split(' ')[1] != 'Klamt':
        ddata = np.array([1.4 for a in range(len(data))])
    else:
        ddata = data[:, 2]
    # Add error analysis for logP (only changing values)
    AveErr, RMS, AUE, tau, R, maxErr, percent = tools.stats_array(data[:,0], exp[:,0], exp[:,1], bootits, dataSet[i])
    # Get data for QQ plot
    X, Y, slope, dslope = tools.getQQdata(data[:,0], exp[:,0], ddata, exp[:,1], bootits)
    line = dataSet[i]
    for met in [AveErr, RMS, AUE, tau, R, maxErr, percent, [slope,dslope]]:
        line = line + ",\t %s +/- %s" % (round_unc(met[0], met[1]), round_sf(met[1], 1))
    output.append(line+'\n')

fileName ='CompareTo16_%.4f.txt' % diff 
f = open(fileName,'w')
f.writelines(output)
f.close()
print "created ", fileName
