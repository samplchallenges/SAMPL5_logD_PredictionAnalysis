# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# May 2016
# Uses checkmol to assign functional group and look for trends 

import commands as c
import sys # For premature exitting while testing the code
import pickle 
import glob
import numpy as np
import imp 
tools = imp.load_source('tools','../DataFiles/tools.py')

#exp = pickle.load(open('../DataFiles/experimental.p','rb'))

# Dictionary with data organized by molecule
moleDict = pickle.load(open('../DataFiles/moleculeData.p'))

# import alphabet list:
alphabet = pickle.load(open('../DataFiles/alphabet.p','rb'))

# Initiate checkmole dictionary
# it will have keys for each functional group with a list of SAMPL5 molecules with that functional group
check = {'z_all': {'molList': []}}

# Check each SAMPL5 molecule
for sid in moleDict.keys():
    # Get checkmol data
    functList = c.getoutput("checkmol ../MoleculeFiles/%s.mol2" % sid) 
    functList = functList.split('\n')
    # Add molecule label to checkmol dictionary
    for funct in functList:
        functKey = funct.replace(',','-')
        # If it doesn't have the functional group key, add it
        if not check.has_key(functKey):
            check[functKey] = {'molList': []}
        
        check[functKey]['molList'].append(sid)
    check['z_all']['molList'].append(sid)

# list of error metrics
metrics = ['AveErr', 'RMS', 'AUE', 'maxErr', 'percent', 'error slope']

# Make header line for data file
output = 'group letter,\tnumber molecules,\t'
for met in metrics:
    output += '%s,\t %s,\t' % (met, 'd'+met)
output = [output+'functional group name\n']
groupOutput = ['letter, functional group, SAMPL5_IDs\n']
# print information from checkmol dictionary
for idx, funct in enumerate(sorted(check.keys())):
    entry = check[funct]
    # Assign letter
    if funct == 'z_all':
        entry['letter'] = 'zz'
    else:    
        entry['letter'] = alphabet[idx]
        groupOutput.append('%s,\t %s, \t\t %s \n' % (entry['letter'], funct, str(sorted(entry['molList']))))

    numMol = len(entry['molList'])
    line = "%s,\t%i,\t" % (entry['letter'], numMol)

    # Get average metrics
    for met in metrics:
        # Calculate average value and uncertainty for molecules in the list
        val = np.average([moleDict[k][met][0] for k in entry['molList']])
        dval = np.average([moleDict[k][met][1] for k in entry['molList']])

        # Save to check mol dictionary
        entry[met] = [val, dval]

        # Add data to output file line
        line += '%.3f,\t %.3f,\t' % (val, dval)

    # save data to output file
    print "%s\n\t%i" % (funct, numMol)
    line += '%s\n' % funct
    output.append(line)


# Save output file
f = open('../DataFiles/checkmolTypes.txt','w')
f.writelines(output)
f.close()

# Save file with SAMPL5 names
f = open('../DataFiles/checkmolGroups.txt','w')
f.writelines(groupOutput)
f.close()

# Now we will make histograms for each metric
keys = sorted(check.keys())
letIDs = [check[k]['letter'] for k in keys if len(check[k]['molList']) > 1]
x_axis = "Checkmol Functional Group Letter"
for m in metrics:
    # Save values to list
    vals = [check[k][m][0] for k in keys]
    dvals = [check[k][m][1] for k in keys]
    
    # File info
    fileName = '../statsPlots/%s_byCheckmolType_large.pdf' % m
    title = 'Checkmol Functional Group'
    # figure out sorting option by type of metric
    if m == 'error slope':
        tools.histPlot(letIDs, vals, dvals, x_axis, m, title, option = 'close to 1', fileName = fileName)
    elif m == 'percent':
        tools.histPlot(letIDs, vals, dvals, x_axis, 'correct sign (%%)', title, option = 'reverse', fileName = fileName)
    else:
        tools.histPlot(letIDs, vals, dvals, x_axis, m, title, fileName = fileName)

print (len(check.keys()))
