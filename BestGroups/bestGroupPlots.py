# Written by Caitlin C Bannan
# Mobley Group, University of California Irvine
# February 2016
# In an attempt to understand bias that might be happening in predictions, we analyzed the results from the top 6 groups (not predictions, we chose 6 sets of predictions in the top 10 by average unsigned error such that no group was represented more than once. 

import pickle
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')
import numpy as np
from sigfig.sigfig import * 
bootits = 1000 # Number of bootstraps

# Numbers we are considering the "best" groups
bestNums = [16,2,73,27,60,40]

# Load all relevant Data
RegData = pickle.load(open('../DataFiles/predictions.p','rb'))
ExpData = pickle.load(open('../DataFiles/experimental.p','rb'))
batches = pickle.load(open('../DataFiles/batches.p','rb'))

# Initiate calculated lists 
Calc = [[],[],[]]
dCalc = [[],[],[]]
AllCalc = []
AlldCalc = []

# Get Experimental Data
Exp = [ [ExpData[k]['data'][0] for k in b] for b in batches ] 
dExp = [ [ExpData[k]['data'][1] for k in b] for b in batches ] 
AllExp = []
AlldExp = []

# Made to store data to return to Andreas Klamt
output = ['# Average of top 6 groups by AUE, submissions 16, 2, 73, 27, 60, adn 40\n', '# SAMPL ID, average logD, uncertainty in average logD (using statistical uncertainty)\n']

# loop through each batch list of sampl molecules
for i,b in enumerate(batches):
    # Add batch label to output data file
    output.append('# Results for batch %i\n' % i)
    
    # for each key in that batch added data to the Calc list
    for k in b:
        print k

        # If k is 083 or 074 print the data for our curiosity, most groups did poorly on these numbers
        if k == 'SAMPL5_083' or k == 'SAMPL5_074':
            for n in bestNums:
                print '\t', RegData[n]['data'][k][0], ' +/- ',  RegData[n]['data'][k][1]

        # Get data for these 6 sets of predictions
        calcList = np.array([RegData[n]['data'][k][0] for n in bestNums]) 
        # Calculate the average predicted value
        calcTemp = np.average(calcList)

        # Propogate the error in each prediction to get an uncertainty for the average
        dcalcTemp = np.average(np.array([RegData[n]['data'][k][1]**2 for n in bestNums]))/np.sqrt(len(calcList)) 

        # add average to list for analysis
        Calc[i].append(calcTemp)
        dCalc[i].append(dcalcTemp)

        # Add data to output file
        data = '%s, %s, %s' % (k, round_unc(calcTemp, dcalcTemp), round_sf(dcalcTemp, 1))
        output.append(data+'\n')

    # Add data to complete list for error analysis
    AllCalc = AllCalc + Calc[i]
    AlldCalc = AlldCalc + dCalc[i]
    AllExp = AllExp + Exp[i]
    AlldExp = AlldExp + dExp[i]

# Save data to output file
fileName = "BestGroups_Data.txt"
f = open(fileName, 'w')
f.writelines(output)
f.close()
print "Made file", fileName

# Get Limits for plot
lowLim = np.min([min(AllCalc), min(AllExp)]) - 1.5
highLim = np.max([max(AllCalc), max(AllExp)]) + 1.5
print "Range: ", lowLim, highLim
print "Error Range", np.min(AlldCalc), np.max(AlldCalc)

# Make comparison plots with average data
title = "Comparing predictions for 'best' 6 groups by AUE"
tools.ComparePlot(Exp, Calc, title, "Experimental logD", "Average Predicted logD", dExp, dCalc, ['batch0','batch1','batch2'], "BestGroups_Compare.pdf", [lowLim, highLim])

# Make QQ plot with average data
title = "QQ Plot for 'best' 6 groups by AUE"
X, Y, slope, dslope = tools.getQQdata(AllCalc, AllExp, AlldCalc, AlldExp, bootits)
tools.makeQQplot(X,Y,slope, title, fileName = "BestGroups_QQ.pdf")

