# Written by Caitlin C Bannan
# Mobley Lab, UC Irvine
# Reads pKa data from Epik log files and stores them in a dictionary 

import glob
import pickle
from sigfig.sigfig import *
import numpy as np
import sys

def dataline(line):
    """
    Tries to split data from line in file, if it splits up then it has pKa data if it doesn't then it's not a data line
    This is very specific to the log files as created by this Epik run, not at all a general use option.
    """
    try:
        data = line.split(' ')
        pKa = float(data[2])
        return True, data[1].strip(), pKa
    except:
        return False, None, None

dictionary = 'dictionary_allResults.p' # this is the dictionary with Mobley Lab data for each molecule
database = pickle.load(open(dictionary,'rb'))
Logs = glob.glob("../MoleculeFiles/*_allpKa.log") 

# Add keys to dictionary:
for k,e in database.items():
    e['Conj_Base'] = []
    e['Conj_Acid'] = []

# Get data from every file
for f in Logs:
    print f
    num = f.split('_')[1]
    samplID = 'SAMPL5_'+num
    # load lines from file
    fil = open(f, 'r')
    lines = fil.readlines()
    fil.close()
    # Find the line with Atom    Acid/Base    pKa    
    for i in range(len(lines)):
        line = lines[i].strip().replace('   ',' ')
        line = line.replace('  ',' ')
        # If it's a data line, get data
        isData, key, pKa = dataline(line)
        if isData:
            # If it is pKa data save it. key will be Conj_Base or Conj_Acid
            database[samplID][key].append(pKa)

# Make lists to save data to write to txt file
relevant = ['SAMPL ID, acidic_pKa, basic_pKa \n']
allpKa = ['SAMPL ID, [all acidic_pKa], [all basic_pKa] \n']

# Save the pKa that would dominate in the acidic and basic case
for k,e in database.items():
    if not e['Conj_Acid']:
        # empty list, no acid hydrogens
        e['pKa_acidic'] = None
    else:
        # lowest pKa will the the first proton to deprotonate so store that
        e['pKa_acidic'] = min(e['Conj_Acid'])

    if not e['Conj_Base']:
        # empty list, no basic pKas
        e['pKa_basic'] = None
    else:
        # Largest pKa will be the first group to protonate, so store it
        e['pKa_basic'] = max(e['Conj_Base'])

    info = '%s, %s, %s' % (k, str(e['pKa_acidic']), str(e['pKa_basic']))
    allInfo = "%s, %s, %s" % (k, str(sorted(e['Conj_Acid'])), str(sorted(e['Conj_Base'], reverse = True)))
    print info
    relevant.append(info+'\n')
    print allInfo
    allpKa.append(allInfo+'\n')

# Save all the collected data to tables so it can be human readable
fN = open('DataTables/pKa_first.txt', 'w')
fN.writelines(relevant)
fN.close()

fN = open('DataTables/pKa_all.txt', 'w')
fN.writelines(allpKa)
fN.close()

# This script uses pKas stored for each molecule to calculate logDs from the predicted logPs 

# Load dictionary
pH = 7.4 # experimental pH

# Start line list for output data file
output = ['SAMPL ID, "logP", acid corrected, base corrected, largest correction\n']

# Loop through dictionary, in order to make data files easier to read
for k in sorted(database.keys()):
    e = database[k]
    # extrack pKas
    pKaAcid = e['pKa_acidic'] 
    pKaBase = e['pKa_basic']

    # Assigne acidic and basic corrections, 0 if there is no pKa
    if pKaAcid == None:
        acid_correction = 0
    else:
        acid_correction = 10**(pH - pKaAcid) 
    if pKaBase == None:
        base_correction = 0
    else:
        base_correction = 10**(pKaBase - pH)

    # extrad logP and uncertainty
    logP = (e['LogD_calc'][0])
    P = 10 ** logP
    dlogD = e['LogD_calc'][1]
    
    # convert P to D using corrections calculated above
    aD = P / (acid_correction + 1)
    bD = P / (base_correction + 1)
    bothD = P / (acid_correction + base_correction + 1)

    # Convert back to logD
    aLogD = np.log10(aD)
    bLogD = np.log10(bD)
    bothLogD = np.log10(bothD)

    # pKa corrections will only decrease the logD value so minimum is the single corrected logD 
    oneLogD =min([aLogD, bLogD, logP]) 

    # Save data to output file list
    output.append('%s,\t\t%s,\t\t%s,\t\t%s,\t\t%s\n' % (k, round_unc(logP, dlogD), round_unc(aLogD, dlogD), round_unc(bLogD, dlogD), round_unc(oneLogD, dlogD)))

    # Save data to dictionary
    e['LogD_acidCorrected'] = [aLogD, dlogD]
    e['LogD_baseCorrected'] = [bLogD, dlogD]
    e['LogD_bothCorrected'] = [bothLogD, dlogD]
    # This assumes the molecule is either an acid or a base, but not both, takes the biggest change 
    e['LogD_oneCorrected'] = [oneLogD, dlogD]

# Save dictionary and data file
pickle.dump(database, open('dictionary_Corrected.p','wb'))
F = open('DataTables/allLogD_pKacorrectedData.txt', 'w')
F.writelines(output)
F.close()


